# Databricks notebook source
# DBTITLE 1,Configure authentication for mounting
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": "appID",
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="key-vault-secrets-2by1-mdw",key="SP-Client-Key"),
           "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<tenantID>/oauth2/token"}

# COMMAND ----------

service_credential = dbutils.secrets.get(scope="key-vault-secrets-2by1-mdw",key="SP-Client-Key")

spark.conf.set("fs.azure.account.auth.type.adls2b1.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.adls2b1.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.adls2b1.dfs.core.windows.net", "appID/clientID")
spark.conf.set("fs.azure.account.oauth2.client.secret.adls2b1.dfs.core.windows.net", service_credential)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.adls2b1.dfs.core.windows.net", "https://login.microsoftonline.com/<tenantID>/oauth2/token")
dbutils.fs.ls("abfss://" + fileSystemName  + "@" + storageAccountName + ".dfs.core.windows.net/")
spark.conf.set("fs.azure.createRemoteFileSystemDuringInitialization", "false")

# COMMAND ----------

# MAGIC %scala
# MAGIC val storageAccountName = "storageAccountName"
# MAGIC val appID = "appID/clientID"
# MAGIC val secret = "*****************************8"
# MAGIC val fileSystemName = "fsName"
# MAGIC val tenantID = "***************"
# MAGIC 
# MAGIC spark.conf.set("fs.azure.account.auth.type." + storageAccountName + ".dfs.core.windows.net", "OAuth")
# MAGIC spark.conf.set("fs.azure.account.oauth.provider.type." + storageAccountName + ".dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.id." + storageAccountName + ".dfs.core.windows.net", "" + appID + "")
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.secret." + storageAccountName + ".dfs.core.windows.net", "" + secret + "")
# MAGIC spark.conf.set("fs.azure.account.oauth2.client.endpoint." + storageAccountName + ".dfs.core.windows.net", "https://login.microsoftonline.com/" + tenantID + "/oauth2/token")
# MAGIC spark.conf.set("fs.azure.createRemoteFileSystemDuringInitialization", "true")
# MAGIC dbutils.fs.ls("abfss://" + fileSystemName  + "@" + storageAccountName + ".dfs.core.windows.net/")
# MAGIC spark.conf.set("fs.azure.createRemoteFileSystemDuringInitialization", "false")

# COMMAND ----------

# MAGIC %fs ls /databricks-datasets/samples/

# COMMAND ----------

# MAGIC %fs mkdirs /databricks-datasets/stockdata

# COMMAND ----------

# DBTITLE 1,Mount filesystem
dbutils.fs.mount(
  source = "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/",
  mount_point = "/mnt/<mount-name>",
  extra_configs = configs)

# COMMAND ----------

# DBTITLE 1,Read Databricks Dataset IoT Devices JSON
df = spark.read.json("dbfs:/databricks-datasets/iot/iot_devices.json")

# COMMAND ----------

# DBTITLE 1,Write IoT Devices JSON
df.write.json("/mnt/<mount-name>/iot_devices.json")

# COMMAND ----------

# DBTITLE 1,List filesystem
dbutils.fs.ls("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/")

# COMMAND ----------

# DBTITLE 1,Read IoT Devices JSON from ADLS Gen2 filesystem
df2 = spark.read.json("abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/iot_devices.json")
display(df2)

# COMMAND ----------

# DBTITLE 1,List mount
dbutils.fs.ls("/mnt/<mount-name>")

# COMMAND ----------

# DBTITLE 1,Read IoT Devices JSON from mount
df2 = spark.read.json("/mnt/<mount-name>/iot_devices.json")
display(df2)

# COMMAND ----------

# DBTITLE 1,Unmount filesystem
dbutils.fs.unmount("/mnt/<mount-name>") 
