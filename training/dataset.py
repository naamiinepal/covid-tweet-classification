import os.path
from typing import Optional
import pandas as pd
from glob import glob
from torch.utils.data import Dataset


class CSVDataset(Dataset):
    def __init__(
        self, dataset_path: str, fold: Optional[int] = None, train: bool = True
    ):
        super().__init__()

        val_filepath = os.path.join(dataset_path, f"fold_{fold}.csv")

        if fold is None:
            self.df = pd.read_csv(dataset_path)["text"].to_numpy()
        elif train:
            train_files = glob(os.path.join(dataset_path, "*.csv"))
            train_files.remove(val_filepath)

            self.df = pd.concat(map(pd.read_csv, train_files))
        else:
            self.df = pd.read_csv(val_filepath)

    def __len__(self) -> int:
        return len(self.df)

    def get_item(self, index):
        return self.df.iloc[index]
