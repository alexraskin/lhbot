#!/bin/bash

set -e

function usage() {
    cat <<USAGE

    Usage: $0 [-u upload] or [-d download]

    Options:
        -u, --upload:   Upload env files from local to s3
        -d --download:  download env files locally from S3
USAGE
    exit 1
}

if [ $# -eq 0 ]; then
    usage
    exit 1
fi

BUCKET_NAME="lhcloudybot-config"

export AWS_PROFILE="lhcloudybot"

while [ "$1" != "" ]; do
    case $1 in
    -u | --upload)
        echo "Uploading files to S3"
        aws s3 cp ./infrastructure/terraform/bot/terraform.tfvars s3://$BUCKET_NAME/terraform.tfvars
        aws s3 cp ./.env s3://$BUCKET_NAME/.env
        echo "Done"
        ;;
    -d | --download)
        shift
        echo "Downloading files from S3"
        aws s3 cp s3://$BUCKET_NAME/terraform.tfvars ./infrastructure/terraform/bot/terraform.tfvars
        aws s3 cp s3://$BUCKET_NAME/.env ./.env
        echo "Done"
        ;;
    -h | --help)
        usage
        ;;
    *)
        usage
        exit 1
        ;;
    esac
    shift
done
