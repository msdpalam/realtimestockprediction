# Modern Data Warehousing and Real-time Analytics with Azure Synapse Analytics and Azure Machine Learning

This step-by-step learning guide takes you through World Wide Importers (WWI) journey to modernize their reporting and analytics environment to a cloud based Analytics platform for both batch and real-time analytics. In the lessons that follow you will learn to:

* Build a meta-data driven pipeline for Synapse Analytics Pipelines and Dataflows, landing data in Azure Data Lake Storage(ADLS)
* Design a logical Enterprise Data Warehouse with Azure Synapse Serverless Pool
* Use Synapse Spark Pools and Notebooks to load data from cloud APIs
* Leverage Power BI to build datasets and reports for near real-time analytics from the Synapse Serverless Analytics endpoint
* Ingest data for real-time analytics using:
  * Azure Event Hub and Azure Stream Analytics
  * Azure Databricks with Azure Synapse Pipelines
  * Azure Synapse Analytics Dataflows and Pipelines
* Develop and training a machine learning model with Azure Machine Learning
* Evaluate the machine learning model with Power BI

**Modern Data Warehousing and Machine Learning with Azure Synapse Analytics and Azure Machine Learning step-by-step** 
<!-- TOC -->
 * [Scenario](#scenario)
 * [Solution architecture](#solution-architecture)
 * [Requirements](#requirements)
  - [Before the hands-on lab](#before-the-hands-on-lab)
  - [Resource naming throughout this lab](#resource-naming-throughout-this-lab)
  - [Exercise 1: Prepare the workload environment](#exercise-1-prepare-the-workload-environment---create-resources-for-the-solution)
    - [Task 1: Create Azure Synapse Workspace](#task-1-create-azure-synapse-workspace)
    - [Task 2: Create Azure Databricks Workspace](#task-2-create-azure-databricks-workspace)
    - [Task 3: Create Azure Machine Learning Workspace](#task-3-create-azure-machine-learning-workspace)
  - [Excercise 2: Implement End to End Batch Analytics Solution](#exercise-2-implement-end-to-end-batch-analytics-solution)
  - [Exercise 3: Implement End to End Real Time Analytics Pipeline](#exercise-3-implement-end-to-end-real-analytics-solution)
  - [Exercise 4: Train, score and consume Machine Learning Model](#exercise-4-train-score-and-consume-machine-learning-model)
<!-- /TOC -->

# Modern Data Warehousing and Machine Learning with Azure Synapse Analytics and Azure Machie Learning step-by-step

## Scenario

Wide World Importers (WWI) is a wholesale novelty goods importer and distributor operating from the San Francisco bay area. They have an on-premises SQL Server data warehouse and are looking for a modern cloud-based solution for both batch and real-time data, ideally in a single platform.​

WWI believe Azure Synapse Analytics is the right platform to achieve their goal of migrating their existing data warehouse to a more scalable and performant platform while providing new insights into their business by incorporating big data analytics.​

Azure offers multiple ways to transform data for Real Time Analytics; WII wanted to evaluate all options to see what was best for their team​

​WWI engaged FastTrack for Azure to help implement an Azure modern data warehouse MVP leveraging Azure Synapse Analytics, Azure ML for Machine Learning, Azure Databricks and Power BI to meet their needs for both batch analytics and real-time big data analytics

## Solution architecture

![Architecture diagram explained in the next paragraph.](media/architecture-mdw.png "Architecture Diagram")

The solution leverages the lambda architecture pattern to handle the ingestion, processing, and analysis of data. This includes:

* Batch processing of big data sources at rest.
* Real-time processing of big data in motion.

Detailed implementation steps are provided in the relevant sections below for batch processing vs real-time analytics.

## Requirements
This learning guide can followed and implemented in it's entirety or you can follow just the batch processing or just the real-time analytics exercises. 

For all exercises, the following is required:

1. Microsoft Azure Subscription
2. Azure Synapse Analytics Workspace
3. Azure Data Lake Storage (can be created automatically as part of your Azure Synapse Analytics Workspace deployment)

For Batch Analytics exercises, the following are also required:

1. Azure SQL Database
2. Power BI Desktop

For Real-Time Analytics exercises, the following are also required:

1. Azure Databricks
2. Azure Machine Learning Workspace / Studio
3. [Python v.3.7 or newer](https://www.python.org/downloads/)
4. [PIP](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)
5. [Visual Studio Code](https://code.visualstudio.com/)
6. [Python Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
7. [Azure Function Core Tools v.3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#v2)
8. [Azure Functions Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
9. [Postman](https://www.postman.com/downloads/)
10. Azure Stream Analytics
10. [Ensure the Microsoft.Sql resource provider is registered in your Azure Subscription](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types).

## Resource naming throughout this lab

For the hands-on walk through, we recommend that you adopt a naming convention, following the guidelines in the article [Define your naming convention](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming). 

## Exercise 1: Prepare the workload environment - create resources for the solution

### Task 1: Create Azure Synapse Workspace

Following [Quickstart: Create a Synapse workspace](https://docs.microsoft.com/en-us/azure/synapse-analytics/quickstart-create-workspace), create your Azure Synapse Workspace. Please note that we are creating other resources like Azure Data Lake Store Gen2 for storage needs

### Task 2: Create Azure Databricks Workspace

Use the Azure portal to create an Azure Databricks workspace with an Apache Spark cluster. For detailed steps, follow the article [Quickstart: Run a Spark job on Azure Databricks Workspace using the Azure portal](https://docs.microsoft.com/en-us/azure/databricks/scenarios/quickstart-create-databricks-workspace-portal?tabs=azure-portal)

### Task 3: Create Azure Machine Learning Workspace

For our machine learning needs, we will leverage Azure Machine Learning, as we see customers love the machine learning studio for model training and inferencing. Use [Quickstart: Create workspace resources you need to get started with Azure Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/quickstart-create-resources)

## Exercise 2: Implement End to End Batch Analytics Solution

For Batch Analytics we will work with relational data.
* We first restored WWImporter database to Azure SQL DB and ran stored procedures to get data through the current date
* We designed a meta-data driven Pipeline approach for loading data from Azure SQL DB to ADLS; this required a small Azure SQL DB to store the data loading logic in a table
* Azure Synapse Pipelines read data from the data load definition database and performs either Copy Data Activities for full-load tables or Dataflow Activities for incremental updates to load the data from the WWImporter Database to Parquet files in ADLS (Bronze Layer)
* A Spark Notebook contains python code to extract the current WWI Stock price throughout the day – this data is used to see if there is any correlation between sales and the stock price as well as get near real time updates of the WWI stock price; The latest stock price for each day is also stored in ADLS
* Serverless SQL Database contains views over the ADLS files to denormalize the data into a Star Schema
* Power BI is leveraged to create a dataset from the SQL Serverless database views along with the reports needed by the end users; The end users will be able to see near-real time orders throughout the day*

## Exercise 3: Implement End to End Real Time Analytics Solution
For real-time analytics scenario, we will leverage yahoo API to generate the real-time data for a date range and stream the data as events.
* To demonstrate real-time analytics capabilities under the same Azure Synapse platform, we are leveraging a data ingestion pipeline through Azure Event Hub. A small program creates an event for rows of data, from yahoo finances snapped for a date range. Once the event shows up, Azure Stream Analytics processes the data and puts the data into Azure Data Lake Store (ADLS Gen2).
* As part of Data Engineering, Azure Databricks mounts the store in Databricks and processes data so we have a prepared dataset that we can build model on. This process is kicked off through Azure Synapse Pipeline (Mount Pipeline + Data Processing Pipeline)

## Exercise 4: Train, Score and Consume Machine Learning Model
* Azure ML picks up the data from ADLS store, trains a model and deploys the model to Azure Container Instance, as a real time endpoint, to predict on the stock price closing trends

