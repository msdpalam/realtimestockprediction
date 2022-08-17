// Databricks notebook source
// MAGIC %md This example notebook closely follows the [Databricks documentation](https://docs.azuredatabricks.net/spark/latest/data-sources/azure/azure-datalake.html) for how to set up Azure Data Lake Store as a data source in Databricks.

// COMMAND ----------

// MAGIC %md ### 0 - Setup
// MAGIC 
// MAGIC To get set up, do these tasks first: 
// MAGIC 
// MAGIC - Get service credentials: Client ID `<aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee>` and Client Credential `<NzQzY2QzYTAtM2I3Zi00NzFmLWI3MGMtMzc4MzRjZmk=>`. Follow the instructions in [Create service principal with portal](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal). 
// MAGIC - Get directory ID `<ffffffff-gggg-hhhh-iiii-jjjjjjjjjjjj>`: This is also referred to as *tenant ID*. Follow the instructions in [Get tenant ID](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal#get-tenant-id). 
// MAGIC - If you haven't set up the service app, follow this [tutorial](https://docs.microsoft.com/en-us/azure/azure-databricks/databricks-extract-load-sql-data-warehouse). Set access at the root directory or desired folder level to the service or everyone.

// COMMAND ----------

// MAGIC %md There are two options to read and write Azure Data Lake data from Azure Databricks:
// MAGIC 1. DBFS mount points
// MAGIC 2. Spark configs
// MAGIC 
// MAGIC We are going to leverage DBFS mount point option to work with ADLS Gen 2, in this example. Note that we are using *scope* and application client key in this example. We can generalize by reading the information in some kind of variables letter

// COMMAND ----------

// MAGIC %md ## 1 - DBFS mount points
// MAGIC [DBFS](https://docs.azuredatabricks.net/user-guide/dbfs-databricks-file-system.html) mount points let you mount Azure Data Lake Store for all users in the workspace. Once it is mounted, the data can be accessed directly via a DBFS path from all clusters, without the need for providing credentials every time. The example below shows how to set up a mount point for Azure Data Lake Store.

// COMMAND ----------

val configs = Map(
  "fs.azure.account.auth.type" -> "OAuth",
  "fs.azure.account.oauth.provider.type" -> "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
  "fs.azure.account.oauth2.client.id" -> "16323797-6396-4120-985b-6f25d2819759",
  "fs.azure.account.oauth2.client.secret" -> dbutils.secrets.get(scope="key-vault-secrets-2by1-mdw",key="SP-Client-Key"),
  "fs.azure.account.oauth2.client.endpoint" -> "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47/oauth2/token")
// Optionally, you can add <directory-name> to the source URI of your mount point.
dbutils.fs.mount(
  source = "abfss://adls2b1fs@adls2b1.dfs.core.windows.net/",
  mountPoint = "/mnt/data-2b1-adls",
  extraConfigs = configs)
