from glob import glob
import os
from typing import Mapping, Optional, Sequence, Union
import numpy as np
import pytorch_lightning as pl

from torch.utils.data import DataLoader

from datasets import load_dataset
from datasets.arrow_dataset import Batch, Example
from transformers import AutoTokenizer, BertTokenizer


class DataModule(pl.LightningDataModule):
    label_names = (
        "covid_stats",
        "vaccination",
        "covid_politics",
        "humour",
        "lockdown",
        "civic_views",
        "life_during_pandemic",
        "covid_waves_and_variants",
    )

    tokenizer_keys = ("input_ids", "token_type_ids", "attention_mask")

    def __init__(
        self,
        model_name_or_path: str,
        dataset_path: str,
        batch_size: int,
        fold: Optional[int] = None,
        max_workers: int = os.cpu_count(),
        pin_memory: bool = True,
    ):
        super().__init__()

        self.save_hyperparameters()

        self.num_workers = min(os.cpu_count(), max_workers)

        self.tokenizer: BertTokenizer = AutoTokenizer.from_pretrained(
            model_name_or_path
        )

    def setup(self, stage: Optional[str] = None) -> None:
        val_filepath = os.path.join(
            self.hparams.dataset_path, f"fold_{self.hparams.fold}.csv"
        )
        if stage is None or stage == "fit":
            train_files = glob(os.path.join(self.hparams.dataset_path, "*.csv"))
            train_files.remove(val_filepath)

            self.train_ds = self.get_tokenized_ds(train_files)
        if stage != "predict":
            self.val_ds = self.get_tokenized_ds(val_filepath)
        if stage is None or stage == "predict":
            self.pred_ds = self.get_tokenized_ds(self.hparams.dataset_path)

    def get_tokenized_ds(
        self,
        data_files: Union[str, Sequence[str]],
    ):
        return (
            load_dataset(
                "csv",
                data_files=data_files,
                split="train",
            )
            .map(self.combine_labels, remove_columns=self.label_names)
            .map(self.batched_tokenize, batched=True, batch_size=256)
        )

    @staticmethod
    def combine_labels(row: Example):
        labels = [row[name] for name in DataModule.label_names]
        return {**row, "labels": labels}

    def batched_tokenize(self, batched_row: Batch):
        text = batched_row.pop("text")
        tokenized_inputs = self.tokenizer(text, truncation=True)
        return {**batched_row, **tokenized_inputs}

    def train_dataloader(self):
        return DataLoader(
            self.train_ds,
            batch_size=self.hparams.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=self.hparams.pin_memory,
        )

    def val_dataloader(self):
        return DataLoader(
            self.train_ds,
            batch_size=self.hparams.batch_size,
            num_workers=self.num_workers,
            pin_memory=self.hparams.pin_memory,
        )

    def pred_dataloader(self):
        return DataLoader(
            self.pred_ds,
            batch_size=self.hparams.batch_size,
            num_workers=self.num_workers,
        )
