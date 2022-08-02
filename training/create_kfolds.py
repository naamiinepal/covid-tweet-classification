import os
from argparse import ArgumentParser, Namespace

import pandas as pd


def main(params: Namespace):
    df = pd.read_csv(params.dataset_file)

    shuffled_df = df.sample(frac=1, ignore_index=True, random_state=params.seed)

    save_dir, ext = os.path.splitext(params.dataset_file)

    os.makedirs(save_dir, exist_ok=True)

    single_fold_length = len(df) / params.folds

    current_length: int = 0

    for i in range(params.folds):
        start_index = i * single_fold_length
        split_df = shuffled_df[int(start_index) : int(start_index + single_fold_length)]
        print(len(split_df))
        current_length += len(split_df)

        split_df.to_csv(os.path.join(save_dir, f"fold_{i+1}{ext}"), index=False)

    print("Final Length", current_length)

    assert (
        len(df) == current_length
    ), "The sum of splitted folds do not equal the original df."


if __name__ == "__main__":
    parser = ArgumentParser(description="Create k-Folds of provided CSV")
    parser.add_argument(
        "--dataset_file",
        default="datasets/nepali_tweets_dataset_labelled_tweets_feb_23.csv",
        help="CSV file with extension",
    )
    parser.add_argument(
        "--folds",
        default=5,
        type=int,
        help="Number of folds",
    )
    parser.add_argument(
        "--seed",
        default=42,
        type=int,
        help="Seed for sampling",
    )

    args = parser.parse_args()

    main(args)
