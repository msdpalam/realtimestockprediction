**Contents** 

<!-- TOC -->
- [Modern Data Warehousing and Machine Learning with Azure Synapse Analytics and Azure Machie Learning step-by-step](#modern-data-warehousing-and-machine-learning-with-azure-synapse-analytics-and-azure-machie-learning-step-by-step)
  - [Scenario](#scenario)
  - [Abstract and learning objectives](#abstract-and-learning-objectives)
  - [Overview](#overview)
  - [Solution architecture](#solution-architecture)
  - [Requirements](#requirements)
  - [Before the hands-on lab](#before-the-hands-on-lab)
  - [Resource naming throughout this lab](#resource-naming-throughout-this-lab)
  - [Exercise 1: Accessing the Azure Synapse Analytics workspace](#exercise-1-accessing-the-azure-synapse-analytics-workspace)
    - [Task 1: Launching Synapse Studio](#task-1-launching-synapse-studio)
 
<!-- /TOC -->

# Modern Data Warehousing and Machine Learning with Azure Synapse Analytics and Azure Machie Learning step-by-step

## Scenario
Wide World Importers (WWI) is a wholesale novelty goods importer and distributor operating from the San Francisco bay area. Currently they have SQL Server based on premise data warehouse solution. They are working on modernizing the solution in the cloud. They reached out to FastTrack for Azure team to help implement a modern data housing solution/POC in Azure, leveraging Azure Synapse, Azure ML for Machine Learning, Azure Databricks and Power BI.

WWI would like to leverage one platform to achieve both their real time and batch analytics goals as part of there innovation and modernization efforts. They believe Azure Synapse Analytics can help them achieve that goal, implementing the solution through Lambda Architecture, a modern big data analytics patterns.

With Azure Synapse platform Serverless SQL Pools, WWI can migrate their existing DW solution with few changes as well as get more frequent updates to their data for reporting  and analytics without the overhead of loading to Dedicated Pools. This will save costs while they further evaluate if, how and when the solution should be moved to a dedicated SQL Pool. Data processing for ML use cases, since they have a lots of realtime data, they wanted a scalable solution, where they can respond to the data growth needs without worrying about cost, whey they do not have any processing needed.
![image](https://user-images.githubusercontent.com/12255455/185238457-ffef0780-3f9c-498e-8394-b50da2765d6e.png)

## Abstract and learning objectives

In this mission is to show case how we can build an end-to-end data advanced analytics solution using Azure Synapse Analytics, Azure Databricks and Azure Machine Learning services. The information will be presented in the context of a retail scenario, as described above. We will be heavily leveraging Azure Synapse Studio, Azure Databricks and Azure Machine Learning Studio as our development tools as we walk through common data operations from ingestion, transformation, querying, model training and visualization. While we can leverage Azure Synapse for all data engineering and data science activites, we wanted to build a scenario where multiple Azure Services could be leveraged to implement the solution, as we see our customers ask for alternate options when building advanced analytics solutions in Azure.

## Overview

In our implementation, we will explore various features of Azure Synapse Analytics, Azure Databricks and Azure Machine Learning Services. Azure Synapse Analytics Studio is a single tool that every team member can use collaboratively, for data engineering needs. We will however leverage Azure Databricks alnog with Synapse Studio, as we ingest, clean, and transform raw data.  We will then leverage Azure Machine Learning Studio to train, register, and consume a Machine learning model. We would like to have hands-on-experience building this solution.



## Solution architecture

![Architecture diagram explained in the next paragraph.](media/architecture-mdw.png "Architecture Diagram")

This walk through leverages the lambda architecture pattern, to handle the ingestion, processing, and analysis of data. We will explore:
* Batch processing of big data sources at rest.
* Real-time processing of big data in motion.

### Batch Analytics
For Batch Analytics we will work with relational data.
* We first restored WWImporter database to Azure SQL DB and ran stored procedures to get data through the current date
* We designed a meta-data driven Pipeline approach for loading data from Azure SQL DB to ADLS; this required a small Azure SQL DB to store the data loading logic in a table
* Azure Synapse Pipelines read data from the data load definition database and performs either Copy Data Activities for full-load tables or Dataflow Activities for incremental updates to load the data from the WWImporter Database to Parquet files in ADLS (Bronze Layer)
* A Spark Notebook contains python code to extract the current WWI Stock price throughout the day – this data is used to see if there is any correlation between sales and the stock price as well as get near real time updates of the WWI stock price; The latest stock price for each day is also stored in ADLS
* Serverless SQL Database contains views over the ADLS files to denormalize the data into a Star Schema
* Power BI is leveraged to create a dataset from the SQL Serverless database views along with the reports needed by the end users; The end users will be able to see near-real time orders throughout the day*

### Real-time Analytics
For real-time analytics scenario, we will leverage yahoo API to generate the real-time data for a date range and stream the data as events.
* To demonstrate real-time analytics capabilities under the same Azure Synapse platform, we are leveraging a data ingestion pipeline through Azure Event Hub. A small program creates an event for rows of data, from yahoo finances snapped for a date range. Once the event shows up, Azure Stream Analytics processes the data and puts the data into Azure Data Lake Store (ADLS Gen2).
* As part of Data Engineering, Azure Databricks mounts the store in Databricks and processes data so we have a prepared dataset that we can build model on. This process is kicked off through Azure Synapse Pipeline (Mount Pipeline + Data Processing Pipeline)

### Machine Learning
* Azure ML picks up the data from ADLS store, trains a model and deploys the model to Azure Container Instance, as a real time endpoint, to predict on the stock price closing trends

The data files we generate during the ingestion and processing will be CSV, and parquet. This data will be ingested into Synapse Analytics via Pipelines. From there, the data can be transformed and enriched using various tools such as data flows, Synapse Spark, Azure Datbricks, and Synapse SQL (both provisioned and serverless). Once processed, data can be queried using Synapse SQL tooling. Azure Synapse Studio also provides the ability to author notebooks to further process data, create datasets, train, and create machine learning models. These models can then be stored in a storage account or even in a SQL table. These models can then be consumed via various methods, including T-SQL. The foundational component supporting all aspects of Azure Synapse Analytics is the ADLS Gen 2 Data Lake.

## Requirements

1. Microsoft Azure subscription

2. Azure Synapse Workspace / Studio

3. [Python v.3.7 or newer](https://www.python.org/downloads/)

4. [PIP](https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip)

5. [Visual Studio Code](https://code.visualstudio.com/)

6. [Python Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

7. [Azure Function Core Tools v.3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#v2)

8. [Azure Functions Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)

9. [Postman](https://www.postman.com/downloads/)

10. [Ensure the Microsoft.Sql resource provider is registered in your Azure Subscription](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/resource-providers-and-types).

## Before the hands-on lab

Refer to the Before the hands-on lab setup guide manual before continuing to the lab exercises.

## Resource naming throughout this lab

For the remainder of this lab, the following terms will be used for various ASA (Azure Synapse Analytics) related resources (make sure you replace them with actual names and values from your environment):

| Azure Synapse Analytics Resource  | To be referred to                                                                  |
|-----------------------------------|------------------------------------------------------------------------------------|
| Azure Subscription                | `WorkspaceSubscription`                                                            |
| Azure Region                      | `WorkspaceRegion`                                                                  |
| Workspace resource group          | `WorkspaceResourceGroup`                                                           |
| Workspace / workspace name        | `asaworkspace{suffix}`                                                             |
| Primary Storage Account           | `asadatalake{suffix}`                                                              |
| Default file system container     | `DefaultFileSystem`                                                                |
| SQL Pool                          | `SqlPool01`                                                                        |
| SQL Serverless Endpoint           | `SqlServerless01`                                                                  |
| Azure Key Vault                   | `asakeyvault{suffix}`                                                              |

## Exercise 1: Accessing the Azure Synapse Analytics workspace


All exercises in this lab utilize the workspace Synapse Studio user interface. This exercise will outline the steps to launch Synapse Studio. Unless otherwise specified, all instruction including menu navigation will occur in Synapse Studio.

### Task 1: Launching Synapse Studio

1. Log into the [Azure Portal](https://portal.azure.com).

2. Expand the left menu, and select the **Resource groups** item.
  
    ![The Azure Portal left menu is expanded with the Resource groups item highlighted.](media/azureportal_leftmenu_resourcegroups.png "Azure Portal Resource Groups menu item")

3. From the list of resource groups, select `WorkspaceResourceGroup`.
  
4. From the list of resources, select the **Synapse Workspace** resource, `asaworkspace{suffix}`.
  
    ![In the resource list, the Synapse Workspace item is selected.](media/resourcelist_synapseworkspace.png "The resource group listing")

5. On the **Overview** tab of the Synapse Workspace page, select the **Open Synapse Studio** card from beneath the **Getting Started** heading. Alternatively, you can select the Workspace web URL link.

    ![On the Synapse workspace resource screen, the Overview pane is shown with the Open Synapse Studio card highlighted. The Workspace web URL value is also highlighted.](media/workspaceresource_launchsynapsestudio.png "Launching Synapse Studio")


