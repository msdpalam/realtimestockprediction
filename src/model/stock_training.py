# Import libraries
from azureml.core import Run
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

# Import libraries
import mlflow
import argparse
import glob
import os



# define functions
def main(args):
    # enable auto logging
    mlflow.autolog()

    # read data
    stock_data = get_csvs_df(args.training_data)
    # load the diabetes dataset
    # print("Loading Data...")
    # stock_data = pd.read_csv('stock_data.csv')

    # process data
    X_train, X_test, y_train, y_test = process_data(stock_data)

    # train model
    train_model(X_train, X_test, y_train, y_test)

def get_csvs_df(path):
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)

def process_data(stock_data):
    # split dataframe into X and y
    x= stock_data[['Open','High','Low']].values
    y= stock_data[['Close']].values

    x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.2,random_state=0)

    # return splits and encoder
    return x_train, x_test, y_train, y_test

def train_model(x_train, x_test, y_train, y_test):
    # train model
    model= LinearRegression()
    model.fit(x_train,y_train)
    LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)
    return model

def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str)
    #parser.add_argument("--reg_rate", dest='reg_rate',
    #                    type=float, default=0.01)

    # parse args
    args = parser.parse_args()

    # return args
    return args


# run script
if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")
