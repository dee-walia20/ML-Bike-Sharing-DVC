from src.utils.all_utils import read_yaml, create_directory
import argparse
import pandas as pd
import zipfile
import os
from io import BytesIO
import requests

def get_data(config_path):
    config = read_yaml(config_path)

    remote_path = config["data_source"]
    remote_file_name = config["data_file_name"]

    artifacts_dir = config["artifacts"]["artifacts_dir"]
    raw_local_dir = config["artifacts"]["raw_local_dir"]
    raw_local_file = config["artifacts"]["raw_local_file"]

    
    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)
    create_directory(dirs=[raw_local_dir_path])
    raw_local_file_path = os.path.join(raw_local_dir_path, raw_local_file)

    #Read the Zip file from URL and pandas.read_csv for specific file.
    req = requests.get(remote_path)
    z = zipfile.ZipFile(BytesIO(req.content))
    df = pd.read_csv(z.open(remote_file_name))

    df.to_csv(raw_local_file_path, sep=",", index=False)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    get_data(config_path=parsed_args.config)