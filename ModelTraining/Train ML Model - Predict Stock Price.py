# Databricks notebook source
# MAGIC %md hi meer
# MAGIC ## Databricks ML: Model Training - Predict Stock Price
# MAGIC 
# MAGIC In this notebook we train machine learning model based on our S&P data that we download (US SPX Data), to predict stock prices on the symbol SPX
# MAGIC 
# MAGIC ### Requirements
# MAGIC - Cluster running Databricks Runtime 7.5 ML or above
# MAGIC 
# MAGIC This notebook is written in **Python** so the default cell type is Python. However, you can use different languages by using the `%LANGUAGE` syntax. Python, Scala, SQL, and R are all supported.

# COMMAND ----------

# MAGIC %md 
# MAGIC ### Load Dependencies

# COMMAND ----------

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt 
from matplotlib import style
plt.style.use( 'bmh')

# COMMAND ----------

# MAGIC %md
# MAGIC ####List the data files we have mounted in DBFS. Please refer to 

# COMMAND ----------

# MAGIC %fs ls /mnt/data-2b1-adls/sandpindexdata/2013

# COMMAND ----------

# MAGIC %md
# MAGIC #### Read Data Into Spark Dataframe

# COMMAND ----------

# File location and type
file_location = "/mnt/data-2b1-adls/sandpindexdata/2013"
file_type = "csv"

# CSV options
infer_schema = "false"
first_row_is_header = "true"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

display(df)

# COMMAND ----------

df.dtypes

# COMMAND ----------

df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC #### Read data into Pandas Data Frame for easy manipulation

# COMMAND ----------

stock_data = pd.read_csv('/dbfs/mnt/data-2b1-adls/sandpindexdata/2013/CleanStockData.csv')

# COMMAND ----------

stock_data.dtypes

# COMMAND ----------

stock_data.head()

# COMMAND ----------

style.use('ggplot')

# COMMAND ----------

x= stock_data[['Open','High','Low']].values
y= stock_data[['Close']].values

x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.2,random_state=0)

regression= LinearRegression()
regression.fit(x_train,y_train)

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)

y_pred= regression.predict(x_test)
result= pd.DataFrame({'Actual':y_test.flatten(),'Predicted':y_pred.flatten()})
result.head(25)

# COMMAND ----------

import math
graph= result.head(25)
graph.plot(kind='bar')

# COMMAND ----------

#Get the number of trading days
stock_data.shape

# COMMAND ----------

#Visualize the close Price Data

plt.figure(figsize=(16,8))
plt.title('Tesla')
plt.xlabel('days')
plt.ylabel('Close price USD($)')
plt.plot(stock_data['Close'])
plt.show()

# COMMAND ----------

#Get the Close price
stock_data_close=stock_data[['Close']]
stock_data_close.head(4)

# COMMAND ----------

#Create a variable to Predict 'x' days out into the future
future_days=25
stock_data['Prediction']=stock_data[['Close']].shift(-future_days)
stock_data.tail(25)

# COMMAND ----------

stock_data.drop(['Prediction'],1)

# COMMAND ----------

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import datetime as dt

plt.figure(figsize = (15, 10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))
x_dates = [dt.datetime.strptime(str(d),'%Y/%m/%d').date() for d in stock_data.index.values]

plt.plot(x_dates, stock_data['High'], label="High")
plt.plot(x_dates, stock_data["Low"], label="Low")
plt.xlabel('Time Scale')
plt.ylabel('Scaled USD')
plt.legend()
plt.gcf().autofmt_xdate()
plt.show()

# COMMAND ----------

# Create a view or table

temp_table_name = "usindex2013"

df.createOrReplaceTempView(temp_table_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC /* Query the created temp table in a SQL cell */
# MAGIC 
# MAGIC select * from `usindex2013`

# COMMAND ----------

# With this registered as a temp view, it will only be available to this particular notebook. If you'd like other users to be able to query this table, you can also create a table from the DataFrame.
# Once saved, this table will persist across cluster restarts as well as allow various users across different notebooks to query this data.
# To do so, choose your table name and uncomment the bottom line.

permanent_table_name = "usstockindex2013"

df.write.format("parquet").saveAsTable(permanent_table_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC /* Query the created temp table in a SQL cell */
# MAGIC 
# MAGIC select * from `usstockindex2013`

# COMMAND ----------

import pandas as pd
stock_data = pd.read_csv('/mnt/data-2b1-adls/sandpindexdata/2013/index_us_sandp_spx.csv', index_col='Date')
# stock_data = pd.read_csv('/mnt/data-2b1-adls/sandpindexdata/2013/index_us_sandp_spx.csv', index_col='Date')
stock_data.head()

# COMMAND ----------

# MAGIC %fs ls /mnt/data-2b1-adls/sandpindexdata/2013

# COMMAND ----------


