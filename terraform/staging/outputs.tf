# This output exposes the name of the created resource group
output "resource_group_name" {
  value = azurerm_resource_group.my_resource_group.name
}

# This output exposes the name of the created AKS cluster
output "kubernetes_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

# This output exposes the name of the created ACR
output "container_registry_name" {
  value = azurerm_container_registry.acr.name
}

# This output exposes the full login server URL of the created ACR
output "container_registry_login_server" {
  value = azurerm_container_registry.acr.login_server
}

# This output exposes the name of the created storage account
output "storage_account_name" {
  value = azurerm_storage_account.my_storage_account.name
}

# This output exposes the primary access key of the staging storage account.
# It is marked as sensitive to prevent it from being displayed in logs.
output "storage_account_primary_key" {
  value     = azurerm_storage_account.my_storage_account.primary_access_key
  sensitive = true
}