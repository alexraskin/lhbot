terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.1"
    }
  }

  required_version = ">= 1.0"
}
