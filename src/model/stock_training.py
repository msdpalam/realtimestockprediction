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

# Get the experiment run context
run = Run.get_context()

# load the diabetes dataset
print("Loading Data...")
stock_data = pd.read_csv('stock_data.csv')

x= stock_data[['Open','High','Low']].values
y= stock_data[['Close']].values

x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.2,random_state=0)

model= LinearRegression()
model.fit(x_train,y_train)

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)

# y_pred= model.predict(x_test)

# calculate accuracy
y_hat= model.predict(x_test)
acc = np.average(y_hat == y_test)
print('Accuracy:', acc)
run.log('Accuracy', np.float(acc))

# # calculate AUC
# y_scores = model.predict_proba(x_test)
# auc = roc_auc_score(y_test,y_scores[:,1])
# print('AUC: ' + str(auc))
# run.log('AUC', np.float(auc))

# Save the trained model in the outputs folder
os.makedirs('outputs', exist_ok=True)
joblib.dump(value=model, filename='outputs/stock_model.pkl')

run.complete()
