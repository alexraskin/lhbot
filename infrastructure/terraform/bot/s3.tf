provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
  default_tags {
    tags = {
      env       = "lhcloudybot"
      terraform = "true"
    }
  }
}

resource "aws_s3_bucket" "lhcloudy_bot_config" {
  bucket = var.lh_bot_s3_bot_config_bucket
  tags = {
    name = var.lh_bot_s3_bot_config_bucket
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lhcloudy_bot_config_server_side_encryption" {
  bucket = aws_s3_bucket.lhcloudy_bot_config.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "lhcloudy_bot_config_public_access_block" {
  bucket = aws_s3_bucket.lhcloudy_bot_config.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "terraform_state_lhbot" {
  bucket = var.lh_bot_s3_terraform_state_bucket
  tags = {
    name = var.lh_bot_s3_terraform_state_bucket
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_lhbot_server_side_encryption" {
  bucket = aws_s3_bucket.terraform_state_lhbot.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state_lhbot_public_access_block" {
  bucket = aws_s3_bucket.terraform_state_lhbot.id

  block_public_acls   = true
  block_public_policy = true
}

resource "aws_s3_bucket" "lhbot_reports_bucket" {
  bucket = var.lh_bot_reports_s3_bucket

  tags = {
    name = var.lh_bot_reports_s3_bucket
  }
}

resource "aws_s3_bucket_policy" "lhbot_bucket_policy" {
  bucket = aws_s3_bucket.lhbot_reports_bucket.id
  policy = data.aws_iam_policy_document.lhbot_bucket_policy.json
}

resource "aws_s3_bucket_public_access_block" "lhbot_reports_bucket_public_access_block" {
  bucket = aws_s3_bucket.lhbot_reports_bucket.id

  block_public_acls   = false
  block_public_policy = false
}


data "aws_iam_policy_document" "lhbot_bucket_policy" {
  statement {
    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }
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

  statement {
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }
    sid    = "KMSdecrypt"
    effect = "Allow"
    actions = [
      "kms:Decrypt",
      "kms:Encrypt",
      "kms:GenerateDataKey",
    ]
    resources = ["*"]
  }
}