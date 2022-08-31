az group create --name '2by1demorg' --location eastus

az deployment group create --resource-group '2by1demorg' --template-file main.bicep --parameters deployazure.parameter.json --verbose