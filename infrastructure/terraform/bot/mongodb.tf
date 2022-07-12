provider "mongodbatlas" {
  public_key  = var.mongodbatlas_public_key
  private_key = var.mongodbatlas_private_key
}

resource "mongodbatlas_cluster" "lhcloudy_cluster" {
  project_id = var.mongodb_project_id
  name       = var.mongodb_cluster_name

  provider_name               = "TENANT"
  backing_provider_name       = "AWS"
  provider_region_name        = "US_EAST_1"
  provider_instance_size_name = "M0"
}

resource "mongodbatlas_database_user" "lhcloudybot_db_user" {
  username           = var.database_user
  password           = var.database_password
  project_id         = var.mongodb_project_id
  auth_database_name = var.mongo_auth_database_name

  roles {
    role_name     = "readWrite"
    database_name = var.mongo_database_name
  }

  labels {
    key   = "Terraform"
    value = "true"
  }

  scopes {
    name = var.mongodb_cluster_name
    type = "CLUSTER"
  }

}
