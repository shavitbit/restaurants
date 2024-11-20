![Architecture view](./image/image.png)


<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | =3.65.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 3.65.0 |
| <a name="provider_random"></a> [random](#provider\_random) | 3.6.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_linux_web_app.app](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/linux_web_app) | resource |
| [azurerm_mssql_database.sql_database](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/mssql_database) | resource |
| [azurerm_mssql_server.sql_server](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/mssql_server) | resource |
| [azurerm_private_dns_a_record.sql_dns_a_record](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/private_dns_a_record) | resource |
| [azurerm_private_dns_zone.sql_private_dns_zone](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/private_dns_zone) | resource |
| [azurerm_private_dns_zone_virtual_network_link.sql_dns_link](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/private_dns_zone_virtual_network_link) | resource |
| [azurerm_private_endpoint.sql_private_endpoint](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/private_endpoint) | resource |
| [azurerm_resource_group.rg](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/resource_group) | resource |
| [azurerm_service_plan.asp](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/service_plan) | resource |
| [azurerm_sql_firewall_rule.azureservicefirewall](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/sql_firewall_rule) | resource |
| [azurerm_subnet.sql_subnet](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/subnet) | resource |
| [azurerm_subnet.subnet](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/subnet) | resource |
| [azurerm_virtual_network.vnet](https://registry.terraform.io/providers/hashicorp/azurerm/3.65.0/docs/resources/virtual_network) | resource |
| [random_password.sqlpassword](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password) | resource |

## Inputs
### APP_PASS AND APP_USER IS ONLY FOR DEVELOPMENT USE! remove them in production or make another variable.tf for production.
### Use it to insert a single record to the database with the secure endpoint in the app for development purposes only (see app documentation)
### For production and to insert unlimited records - use the SSDT CI/CD flow
| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_APP_PASS"></a> [APP\_PASS](#input\_APP\_PASS) | application password to add record the database. | `string` | `"psdfm@lfo3asd5fko9asdk"` | no |
| <a name="input_APP_USER"></a> [APP\_USER](#input\_APP\_USER) | application user to add record the database | `string` | `"adminoren"` | no |
| <a name="input_resource_group_location"></a> [resource\_group\_location](#input\_resource\_group\_location) | resource group location | `string` | `"West Europe"` | no |
| <a name="input_resource_group_name"></a> [resource\_group\_name](#input\_resource\_group\_name) | The name of the resource group | `string` | `"restaurant-recommendation-rg"` | no |
| <a name="input_web_app_name"></a> [web\_app\_name](#input\_web\_app\_name) | name of the web app | `string` | `"restaurant-api-app-dev1"` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_mssql_admin_password"></a> [mssql\_admin\_password](#output\_mssql\_admin\_password) | The MSSQL server password |
<!-- END_TF_DOCS -->