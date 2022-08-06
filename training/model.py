from typing import Optional, Union

import pytorch_lightning as pl
import torch
import torchmetrics as tm
from torch import nn
from transformers import (
    AutoModelForSequenceClassification,
    get_polynomial_decay_schedule_with_warmup,
)
from transformers.modeling_outputs import SequenceClassifierOutput
from datamodule import DataModule


class LightningModel(pl.LightningModule):

    no_decay_params = {"bias", "LayerNorm.weight"}

    def __init__(
        self,
        model_name_or_path: str,
        num_labels: int,
        learning_rate: float = 5e-5,
        warmup_ratio: float = 0.1,
        weight_decay: float = 0.01,
        dropout_rate: float = 0.4,
        calc_bias: bool = True,
    ):
        super().__init__()

        self.save_hyperparameters()

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name_or_path,
            num_labels=num_labels,
            problem_type="multi_label_classification",
            classifier_dropout=dropout_rate,
        )

    def setup(self, stage: Optional[str] = None) -> None:
        if (stage is None or stage == "fit") and self.hparams.calc_bias:
            # Get labels as a pandas dataframe
            train_labels = torch.as_tensor(self.trainer.datamodule.train_ds["labels"])

            # Calculate bias from the training dataset
            bias_initializer = train_labels.mean(axis=0, dtype=torch.float32).log()

            # Override classifier bias
            self.model.classifier.bias = nn.Parameter(bias_initializer)

    def forward(self, inputs: dict) -> SequenceClassifierOutput:
        return self.model(**inputs)

    def training_step(self, batch: dict, batch_idx: int):
        labels = batch.pop("labels")

        # Convert to float to calculate loss
        model_pred = self({**batch, "labels": labels.float()})

        logits = model_pred.logits

        self.log_metrics(logits, labels, "train")

        loss = model_pred.loss
        self.log("train_loss", loss)

        return loss

    def validation_step(self, batch: dict, batch_idx: int, dataloader_idx: int = 0):
        labels = batch.pop("labels")

        # Convert to float to calculate loss
        model_pred = self({**batch, "labels": labels.float()})

        logits = model_pred.logits

        self.log_metrics(logits, labels, "val")

        loss = model_pred.loss
        self.log("val_loss", loss, prog_bar=True, sync_dist=True)

    def log_metrics(self, *metrics_args: Union[torch.Tensor, str]):
        self.log_auc(*metrics_args)
        self.log_f1score(*metrics_args)
        self.log_stat_scores(*metrics_args)

    def log_auc(self, logits: torch.Tensor, labels: torch.Tensor, step: str):
        precision, recall, _ = tm.functional.precision_recall_curve(
            logits, labels, self.hparams.num_labels
        )

        auc = tuple(tm.functional.auc(p, r) for p, r in zip(precision, recall))

        log_prefix = f"{step}_auc_"

        for lab, value in zip(DataModule.label_names, auc):
            self.log(f"{log_prefix}{lab}", value, sync_dist=True)

        self.log(f"{log_prefix}mean", torch.stack(auc).mean(), sync_dist=True)

    def log_f1score(self, logits: torch.Tensor, labels: torch.Tensor, step: str):
        f1_score = tm.functional.f1_score(
            logits, labels, average=None, num_classes=self.hparams.num_labels
        )

        log_prefix = f"{step}_f1score_"

        for lab, value in zip(DataModule.label_names, f1_score):
            self.log(f"{log_prefix}{lab}", value, sync_dist=True)

        self.log(f"{log_prefix}mean", f1_score.mean(), sync_dist=True)

    def log_stat_scores(self, logits: torch.Tensor, labels: torch.Tensor, step: str):
        # tp, fp, tn, fn, support
        stat_scores = tm.functional.stat_scores(
            logits, labels, reduce="macro", num_classes=self.hparams.num_labels
        ).float()

        stat_scores_names = ("tp", "fp", "tn", "fn", "support")

        for lab, score in zip(DataModule.label_names, stat_scores):
            for name, value in zip(stat_scores_names, score):
                # The logger logs only float tensors
                self.log(f"{step}_{name}_{lab}", value, sync_dist=True)

        for name, value in zip(stat_scores_names, stat_scores.mean(0)):
            self.log(f"{step}_{name}_mean", value, sync_dist=True)

    def predict_step(self, batch: dict, batch_idx: int, dataloader_idx: int = 0):
        return self(batch).logits >= 0.5

    def configure_optimizers(self):
        optimizer_grouped_parameters = [
            {
                "params": [
                    p
                    for n, p in self.named_parameters()
                    if not any(nd in n for nd in self.no_decay_params)
                ],
                "weight_decay": self.hparams.weight_decay,
            },
            {
                "params": [
                    p
                    for n, p in self.named_parameters()
                    if any(nd in n for nd in self.no_decay_params)
                ],
                "weight_decay": 0,
            },
        ]

        optimizer = torch.optim.AdamW(
            optimizer_grouped_parameters, lr=self.hparams.learning_rate
        )

        total_steps = self.trainer.estimated_stepping_batches

        scheduler = {
            "scheduler": get_polynomial_decay_schedule_with_warmup(
                optimizer,
                num_warmup_steps=self.hparams.warmup_ratio * total_steps,
                num_training_steps=total_steps,
            ),
            "interval": "step",
            "frequency": 1,
        }

        return [optimizer], [scheduler]
