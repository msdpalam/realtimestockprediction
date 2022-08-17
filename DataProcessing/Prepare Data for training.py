# Databricks notebook source
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
# MAGIC #### Convert Spark Data Frame into Pandas Data Frame for easy manipulation

# COMMAND ----------

stock_data = df.toPandas()

# COMMAND ----------

stock_data.dtypes

# COMMAND ----------

stock_data.convert_dtypes()

# COMMAND ----------

stock_data.dtypes

# COMMAND ----------

stock_data['Open'] = stock_data['Open'].apply(lambda x: float(x.split()[0].replace(',', '')))
stock_data['High'] = stock_data['High'].apply(lambda x: float(x.split()[0].replace(',', '')))
stock_data['Low'] = stock_data['Low'].apply(lambda x: float(x.split()[0].replace(',', '')))
stock_data['Close'] = stock_data['Close'].apply(lambda x: float(x.split()[0].replace(',', '')))

# COMMAND ----------

stock_data.dtypes

# COMMAND ----------

stock_data.head()

# COMMAND ----------

stock_data.head(100)

# COMMAND ----------

style.use('ggplot')

# COMMAND ----------

stock_data.head(25)

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

# MAGIC %fs ls /databricks-datasets

# COMMAND ----------

# MAGIC %fs ls /mnt/data-2b1-adls/sandpindexdata/2013

# COMMAND ----------

stock_data.to_csv('/dbfs/mnt/data-2b1-adls/sandpindexdata/2013/CleanStockData.csv', sep=',', header=True, index=False)

# COMMAND ----------

import os

outname = 'CleanStockData1.csv'

outdir = '/dbfs/mnt/data-2b1-adls/sandpindexdata/2013'
if not os.path.exists(outdir):
    os.mkdir(outdir)

fullname = os.path.join(outdir, outname)    

stock_data.to_csv(fullname)
# stock_data.to_csv('/databricks-datasets/CleanStockData.csv')


# COMMAND ----------


