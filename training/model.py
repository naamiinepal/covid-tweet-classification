from typing import Optional

import pytorch_lightning as pl
import torch
import torchmetrics
from torch import nn
from transformers import (
    AutoModel,
    AutoModelForSequenceClassification,
    get_polynomial_decay_schedule_with_warmup,
)
from transformers.modeling_outputs import SequenceClassifierOutput


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

        self.train_auc = torchmetrics.AUC()
        self.train_f1score = torchmetrics.F1Score(
            num_classes=num_labels, average="weighted"
        )
        self.train_stat_scores = torchmetrics.StatScores(
            num_classes=num_labels, reduce="macro"
        )

        self.val_auc = torchmetrics.AUC()
        self.val_f1score = torchmetrics.F1Score(
            num_classes=num_labels, average="weighted"
        )
        self.val_stat_scores = torchmetrics.StatScores(
            num_classes=num_labels, reduce="macro"
        )

    def prepare_data(self) -> None:
        AutoModel.from_pretrained(self.hparams.model_name_or_path)

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
        model_pred = self(batch)

        logits = model_pred.logits
        labels = batch["labels"]

        self.update_auc(logits, labels, self.train_auc)
        self.log("train_auc", self.train_auc)

        self.train_f1score(logits, labels)
        self.log("train_f1score", self.train_f1score)

        self.train_stat_scores(logits, labels)
        self.log("train_stat_scores", self.train_stat_scores)

        loss = model_pred.loss
        self.log("train_loss", loss)

        return loss

    def validation_step(self, batch: dict, batch_idx: int, dataloader_idx: int = 0):
        model_pred = self(batch)

        logits = model_pred.logits
        labels = batch["labels"]

        self.update_auc(logits, labels, self.val_auc)
        self.log("val_auc", self.val_auc)

        self.val_f1score(logits, labels)
        self.log("val_f1score", self.val_f1score)

        self.val_stat_scores(logits, labels)
        self.log("val_stat_scores", self.val_stat_scores)

        loss = model_pred.loss
        self.log("val_loss", loss)

    def update_auc(
        self, logits: torch.Tensor, labels: torch.Tensor, auc_tracker: torchmetrics.AUC
    ):
        """
        Update internal state of the provided `auc_tracker`
        """
        precision, recall, _ = torchmetrics.functional.precision_recall_curve(
            logits, labels, self.hparams.num_labels
        )

        auc_tracker(precision, recall)

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
