terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.1"
    }
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
      version = "~> 4.22"
    }
    github = {
      source  = "integrations/github"
      version = "~> 5.3.0"
    }
  }
  required_version = ">= 1.0"
}
