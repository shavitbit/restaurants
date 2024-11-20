
variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "restaurant-recommendation-rg" 
}

variable "resource_group_location" {
  description = "resource group location"
  type        = string
  default     = "West Europe" 
}

variable "web_app_name" {
  description = "name of the web app" ####If you change it you will have to change the pipeline. Joe Biden: Dont!
  type        = string
  default     = "restaurant-api-app-dev1" 
}

variable "tags" {
  description = "A map of tags to apply to all resources"
  type        = map(string)
  default     = {
    Environment = "dev"
    Project     = "restaurants"
  }
}
#APP_PASS AND APP_USER IS ONLY FOR DEVELOPMENT USE! for remove them in production or make another variable.tf for production.
#use it to insert a single record to the database with the secure endpoint in the app (see app documentation)
#For production and to insert unlimited records - use the SSDT CI/CD flow
variable "APP_PASS" {
  description = "application password to add record the database"
  type        = string
  default     = "psdfm@lfo3asd5fko9asdk"
}

variable "APP_USER" {
  description = "application user to add record the database"
  type        = string
  default     = "adminoren"
}