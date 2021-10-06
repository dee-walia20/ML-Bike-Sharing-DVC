from src.utils.all_utils import read_yaml, create_directory
import argparse
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
import joblib

def train(config_path, params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    artifacts_dir = config["artifacts"]["artifacts_dir"]
    split_data_dir = config["artifacts"]["split_local_dir"]
   
    train_data_file = config["artifacts"]["train"]
    train_data_path = os.path.join(artifacts_dir, split_data_dir, train_data_file)

    train_data = pd.read_csv(train_data_path)
    train_x = train_data.drop(columns=["dteday", "cnt"], axis=1)
    train_y = train_data["cnt"]
    
    encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value= -1)
    
    n_jobs = params["model_params"]["RF"]["n_jobs"]
    random_state = params["model_params"]["RF"]["random_state"]
    n_estimators = params["model_params"]["RF"]["n_estimators"]

    rf = RandomForestRegressor(n_jobs=n_jobs, n_estimators=n_estimators, random_state=random_state)
    
    pipeline = Pipeline(steps=[('encoder',encoder), ('rf', rf)])
    pipeline.fit(train_x, train_y)
    print("Training is completed")
    
    model_dir = config["artifacts"]["model_dir"]
    model_filename = config["artifacts"]["model_filename"]
    model_dir = os.path.join(artifacts_dir, model_dir)
    
    create_directory([model_dir])
    model_path = os.path.join(model_dir, model_filename)
    joblib.dump(pipeline, model_path)
    print("Model is saved")

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()
    train(config_path= parsed_args.config, params_path= parsed_args.params)