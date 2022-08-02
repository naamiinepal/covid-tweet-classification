import numpy as np

from datamodule import DataModule

dm = DataModule(
    model_name_or_path="google/muril-base-cased",
    dataset_path="datasets/nepali_tweets_dataset_labelled_tweets_feb_23",
    batch_size=32,
    fold=1,
    pin_memory=False,
)

dm.setup("fit")

labels = np.asarray(dm.train_ds["labels"], dtype=bool)

expect_prob = labels.mean(axis=0, dtype=np.float32)

assert np.all(expect_prob), "Any one of the expected prob is zero."
