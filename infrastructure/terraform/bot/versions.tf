terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.1"
    }
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "1.4.1"
    }
    sentry = {
      source  = "jianyuan/sentry"
      version = "0.9.2"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "4.22.0"
    }
  }
  required_version = ">= 1.0"
}
