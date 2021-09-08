import pandas as pd
import argparse
from src.utils.common_utils import (
    read_params,
    create_dir,
    save_local_df,
)
from sklearn.model_selection import train_test_split
import logging

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=logging_str)




def split_and_save_data(config_path):
    config = read_params(config_path)

    artifacts = config["artifacts"]

    raw_local_data = artifacts["raw_local_data"]

    split_data = artifacts["split_data"]
    processed_data_dir = split_data["processed_data_dir"]
    test_data_path = split_data["test_path"]
    train_data_path = split_data["train_path"]

    create_dir([processed_data_dir])

    base = config["base"]
    split_ratio = base["test_size"]
    random_seed = base["random_state"]

    df = pd.read_csv(raw_local_data, sep=",")

    train, test = train_test_split(df, test_size=split_ratio, random_state=random_seed)

    for data, data_path in (test, test_data_path), (train, train_data_path):
        save_local_df(data, data_path)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        data = split_and_save_data(config_path=parsed_args.config)
        logging.info("split data stage completed")
    except Exception as e:
        logging.error(e)
        # raise e
