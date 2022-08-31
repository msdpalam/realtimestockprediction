param workspaceName string
param workspaceLocation string
param defaultSynapseStorageAccountName string
param defaultSynapseStorageAccountFileSystemName string
param sqlAdministratorUsername string
@secure()
param sqlAdministratorPassword string
param datalakeStoreName string
param storageAccountType string
param storageContainerNames array = [
  'default'
]

//https://github.com/mattias-fjellstrom/azure-bicep-upload-data-to-storage/blob/main/modules/blob.bicep

resource datalakeStoreGen2 'Microsoft.Storage/storageAccounts@2021-09-01' = {
  name: datalakeStoreName
  kind: 'StorageV2'
  location: workspaceLocation
  
  properties:{
    minimumTlsVersion: 'TLS1_2'
    isHnsEnabled: true
    accessTier: 'Hot'
  }
  sku: {
    name: storageAccountType
  }
  
}

resource storageBlobServices 'Microsoft.Storage/storageAccounts/blobServices@2021-02-01' = {
  parent: datalakeStoreGen2
  name: 'default'
  properties: {
    containerDeleteRetentionPolicy: {
      enabled: true
      days: 7
    }
    cors: {
      corsRules: []
    }
  }
}

resource storageContainers 'Microsoft.Storage/storageAccounts/blobServices/containers@2021-02-01' = [for storageContainerName in storageContainerNames: {
  parent: storageBlobServices
  name: storageContainerName
  properties: {
    publicAccess: 'None'
    metadata: {}
  }
}]

// Resources
resource synapse 'Microsoft.Synapse/workspaces@2021-06-01' = {
  name: workspaceName
  location: workspaceLocation
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    defaultDataLakeStorage: {
      //How to refer to storage - https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#environment
      // https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-deployment#environment
      //Do not hardcode
      accountUrl: 'https://${defaultSynapseStorageAccountName}.dfs.${environment().suffixes.storage}'
      filesystem: defaultSynapseStorageAccountFileSystemName
    }
    sqlAdministratorLogin: sqlAdministratorUsername
    sqlAdministratorLoginPassword: sqlAdministratorPassword
  }
}
