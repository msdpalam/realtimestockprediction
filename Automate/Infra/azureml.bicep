// https://medium.com/codex/using-bicep-to-create-workspace-resources-and-get-started-with-azure-machine-learning-bcc57fd4fd09

param mlStorageAccountName string
var tenantId = subscription().tenantId
param location string
//var storageAccountName_var = 'st${name}${environment}'
param mlKeyvaultName string
//var keyVaultName_var = 'kv-${name}-${environment}'
param mlAppInsightName string
//var applicationInsightsName_var = 'appi-${name}-${environment}'
param mlContainerRegistryName string
//var containerRegistryName_var = 'cr${name}${environment}'
param mlWorkspaceName string
//var workspaceName_var = 'mlw${name}${environment}'
var storageAccount = storageAccountName.id
var keyVault = keyVaultName.id
var applicationInsights = applicationInsightsName.id
var containerRegistry = containerRegistryName.id

resource storageAccountName 'Microsoft.Storage/storageAccounts@2021-01-01' = {
  name: mlStorageAccountName
  location: location
  sku: {
    name: 'Standard_RAGRS'
  }
  kind: 'StorageV2'
  properties: {
    encryption: {
      services: {
        blob: {
          enabled: true
        }
        file: {
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    supportsHttpsTrafficOnly: true
  }
}
resource keyVaultName 'Microsoft.KeyVault/vaults@2021-04-01-preview' = {
  name: mlKeyvaultName
  location: location
  properties: {
    tenantId: tenantId
    sku: {
      name: 'standard'
      family: 'A'
    }
    accessPolicies: []
    enableSoftDelete: true
  }
}
resource applicationInsightsName 'Microsoft.Insights/components@2020-02-02' = {
  name: mlAppInsightName
  location: location//(((location == 'eastus2') || (location == 'westcentralus')) ? 'southcentralus' : location)
  kind: 'web'
  properties: {
    Application_Type: 'web'
  }
}
resource containerRegistryName 'Microsoft.ContainerRegistry/registries@2019-12-01-preview' = {
  sku: {
    name: 'Standard'
  }
  name: mlContainerRegistryName
  location: location
  properties: {
    adminUserEnabled: true
  }
}
resource workspaceName 'Microsoft.MachineLearningServices/workspaces@2021-07-01' = {
  identity: {
    type: 'SystemAssigned'
  }
  name: mlWorkspaceName
  location: location
  properties: {
    friendlyName: mlWorkspaceName
    storageAccount: storageAccount
    keyVault: keyVault
    applicationInsights: applicationInsights
    containerRegistry: containerRegistry
    //hbiWorkspace: hbi_workspace
  }
  /*
  dependsOn: [
    storageAccountName
    keyVaultName
    applicationInsightsName
    containerRegistryName
  ]
  */
}
