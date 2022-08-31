//scope
targetScope = 'resourceGroup'


param defaultSynapseStorageAccountName string
param defaultSynapseStorageAccountFileSystemName string

param sqlAdministratorUsername string
@secure()
param sqlAdministratorPassword string
param datalakeStoreName string
param location string
param storageAccountType string
param synapseWorkspaceName string

param mlStorageAccountName string

//var storageAccountName_var = 'st${name}${environment}'
param mlKeyvaultName string
//var keyVaultName_var = 'kv-${name}-${environment}'
param mlAppInsightName string
//var applicationInsightsName_var = 'appi-${name}-${environment}'
param mlContainerRegistryName string
//var containerRegistryName_var = 'cr${name}${environment}'
param mlWorkspaceName string

/*
// General parameters
@description('Specifies the location for synapse.')
param location string

@description('Specifies the administrator password of the sql servers in Synapse. If you selected dataFactory as processingService, leave this value empty as is.')
param sqlAdministratorPassword string = ''

@description('Specifies the resource ID of the default storage account file system for Synapse. If you selected dataFactory as processingService, leave this value empty as is.')
param synapseDefaultStorageAccountFileSystemId string = ''

@description('Specifies whether an Azure SQL Pool should be deployed inside your Synapse workspace as part of the template. If you selected dataFactory as processingService, leave this value as is.')
param enableSqlPool bool = false

*/

//var synapseWorkspaceName = 'synapse001'

module synapse001 'deploysynapse.bicep' = {
  name: 'synapse001'
  scope: resourceGroup()
  params: {
    workspaceLocation: location
    workspaceName: synapseWorkspaceName
    sqlAdministratorUsername: sqlAdministratorUsername
    sqlAdministratorPassword: sqlAdministratorPassword
    defaultSynapseStorageAccountName:defaultSynapseStorageAccountName
    defaultSynapseStorageAccountFileSystemName:defaultSynapseStorageAccountFileSystemName
    storageAccountType: storageAccountType
    datalakeStoreName: datalakeStoreName
  }
}

module azureml001 'azureml.bicep' ={
  name: 'azureml001'  
  scope: resourceGroup()
  params:{
    location:location
    mlStorageAccountName: mlStorageAccountName
    mlAppInsightName: mlAppInsightName
    mlContainerRegistryName: mlContainerRegistryName
    mlKeyvaultName: mlKeyvaultName
    mlWorkspaceName: mlWorkspaceName
  }

}

//param utcValue string = utcNow()

/*
var randomstring = toLower(replace(uniqueString(subscription().id, resourceGroup().id, utcValue), '-', ''))
//param ipaddress string
var workspaceName = 'synapse${randomstring}'
param sqlAdministratorLogin string
@secure()
param sqlAdministratorLoginPassword string
var blobName = 'storage${randomstring}'
param storageAccountType string
param sqlpoolName string
param bigDataPoolName string
param nodeSize string
param sparkPoolMinNodeCount int
param sparkPoolMaxNodeCount int
param defaultDataLakeStorageFilesystemName string
param collation string
//param userObjectId string
param dataLakeUrlFormat string
param location string
*/
/*
//Storage account for deployment scripts
module synapsedeploy 'synapsews.bicep' = {
  name: 'synapsed'
  params: {
    synapseName: workspaceName
    location: location
    sqlAdministratorLogin: sqlAdministratorLogin
    sqlAdministratorLoginPassword: sqlAdministratorLoginPassword
    blobName: blobName
    storageAccountType: storageAccountType
    sqlpoolName: sqlpoolName
    bigDataPoolName: bigDataPoolName
    nodeSize: nodeSize
    sparkPoolMinNodeCount: sparkPoolMinNodeCount
    sparkPoolMaxNodeCount: sparkPoolMaxNodeCount
    defaultDataLakeStorageFilesystemName: defaultDataLakeStorageFilesystemName
    collation: collation
    //userObjectId: userObjectId
    dataLakeUrlFormat: dataLakeUrlFormat
  }
}

output resourceSuffix string = randomstring


*/
