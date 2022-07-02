#!/bin/bash

set -e

BUCKET_NAME="lhcloudybot-config"

aws s3 cp s3://$BUCKET_NAME/terraform.tfvars ./infrastructure/terraform/terraform.tfvars

aws s3 cp s3://$BUCKET_NAME/.env ./.env
