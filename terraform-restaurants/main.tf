# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.65.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  skip_provider_registration = true
  features {}
}
# Random password for sql server
provider "random" {}

resource "random_password" "sqlpassword" {
  length  = 16
  special = true
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.resource_group_location
  tags = var.tags
}

# Network
resource "azurerm_virtual_network" "vnet" {
  name                = "restaurant-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  tags = var.tags
}

resource "azurerm_subnet" "subnet" {
  name                 = "restaurant-subnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "delegation"

    service_delegation {
      name = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "sql_subnet" {
  name                 = "sql-subnet"
  resource_group_name  = var.resource_group_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]
}

# SQL
resource "azurerm_mssql_server" "sql_server" {
  name                          = "restaurant-sql-server"
  resource_group_name           = var.resource_group_name
  location                      = var.resource_group_location
  version                       = "12.0"
  administrator_login           = "sqladmin"
  administrator_login_password  = random_password.sqlpassword.result
  tags = var.tags
}

output "mssql_admin_password" {
  value       = random_password.sqlpassword.result
  sensitive   = true
  description = "The MSSQL server password"
}

resource "azurerm_mssql_database" "sql_database" {
  name = "restaurantdb"
  server_id = azurerm_mssql_server.sql_server.id
  sku_name  = "S0"
  tags = var.tags
}

resource "azurerm_sql_firewall_rule" "azureservicefirewall" {
  name                = "allow-azure-service"
  resource_group_name = var.resource_group_name
  server_name         = azurerm_mssql_server.sql_server.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}

# Private endPoint for SQL
resource "azurerm_private_endpoint" "sql_private_endpoint" {
  name                = "sql-private-endpoint"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  subnet_id           = azurerm_subnet.sql_subnet.id
  tags = var.tags

  private_service_connection {
    name                           = "sql-private-connection"
    private_connection_resource_id = azurerm_mssql_server.sql_server.id
    subresource_names              = ["sqlServer"]
    is_manual_connection           = false
  }
}

resource "azurerm_private_dns_zone" "sql_private_dns_zone" {
  name                = "privatelink.database.windows.net"
  resource_group_name = var.resource_group_name
  tags = var.tags
}

resource "azurerm_private_dns_zone_virtual_network_link" "sql_dns_link" {
  name                  = "sql-dns-link"
  resource_group_name   = var.resource_group_name
  private_dns_zone_name = azurerm_private_dns_zone.sql_private_dns_zone.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
  tags = var.tags
}

resource "azurerm_private_dns_a_record" "sql_dns_a_record" {
  name                = azurerm_mssql_server.sql_server.name
  zone_name           = azurerm_private_dns_zone.sql_private_dns_zone.name
  resource_group_name = var.resource_group_name
  ttl                 = 300
  records             = [azurerm_private_endpoint.sql_private_endpoint.private_service_connection[0].private_ip_address]
  tags = var.tags
}

# App Service
resource "azurerm_service_plan" "asp" {
  name                = "restaurant-asp"
  location            = var.resource_group_location
  resource_group_name = var.resource_group_name
  sku_name            = "B1"
  os_type             = "Linux"
  tags = var.tags
}

resource "azurerm_linux_web_app" "app" {
  name                = var.web_app_name
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  service_plan_id     = azurerm_service_plan.asp.id
  public_network_access_enabled = true
  virtual_network_subnet_id = azurerm_subnet.subnet.id
  tags = var.tags

  site_config {
    application_stack{
      python_version = 3.8
    }
  }
  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = "false"
    WEBSITES_PORT                       = "5000"
    SQL_PASS =  random_password.sqlpassword.result
    SQL_USER = azurerm_mssql_server.sql_server.administrator_login
    SQLDB = azurerm_mssql_database.sql_database.name
    SQL_server = azurerm_mssql_server.sql_server.fully_qualified_domain_name
    APP_PASS = var.APP_PASS
    APP_USER = var.APP_USER

  }
}