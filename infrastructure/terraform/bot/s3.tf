provider "aws" {
  profile = "lhcloudybot"
  region  = "us-east-1"
}

resource "aws_s3_bucket" "lhcloudy_bot_config" {
  bucket = var.lh_bot_s3_bot_config_bucket
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    terraform = "true"
    name      = var.lh_bot_s3_bot_config_bucket
  }
}

resource "aws_s3_bucket_public_access_block" "lhcloudy_bot_config_public_access_block" {
  bucket = aws_s3_bucket.lhcloudy_bot_config.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "terraform_state_lhbot" {
  bucket = var.lh_bot_s3_terraform_state_bucket
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    terraform = "true"
    name      = var.lh_bot_s3_terraform_state_bucket
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state_lhbot_public_access_block" {
  bucket = aws_s3_bucket.terraform_state_lhbot.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "lhbot_reports_bucket" {
  bucket = var.lh_bot_reports_s3_bucket
  policy = data.aws_iam_policy_document.lhbot_bucket_policy.json

  tags = {
    terraform = "true"
    name      = var.lh_bot_reports_s3_bucket
  }
}

data "aws_iam_policy_document" "lhbot_bucket_policy" {
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:GetObject",
      "s3:GetObjectAcl",
      "s3:DeleteObject"
    ]
    resources = ["arn:aws:s3:::lhbot",
    "arn:aws:s3:::lhbot/*"]
  }
}
