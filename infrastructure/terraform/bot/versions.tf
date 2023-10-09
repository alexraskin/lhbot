terraform {
  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.6"
    }
    sentry = {
      source  = "jianyuan/sentry"
      version = "~> 0.9"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.42"
    }
    github = {
      source  = "integrations/github"
      version = "~> 5.3.0"
    }
    railway = {
      source  = "terraform-community-providers/railway"
      version = "0.2.0"
    }
  }
  required_version = ">= 1.0"
}
