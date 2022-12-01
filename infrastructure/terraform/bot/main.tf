terraform {
  backend "s3" {
    bucket  = "terraform-state-lhbot"
    key     = "terraform.tfstate"
    encrypt = true
    region  = "us-east-1"
    profile = "default"
  }
}
