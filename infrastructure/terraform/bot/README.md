# bot

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | 4.22.0 |
| <a name="requirement_heroku"></a> [heroku](#requirement\_heroku) | ~> 5.1 |
| <a name="requirement_mongodbatlas"></a> [mongodbatlas](#requirement\_mongodbatlas) | 1.4.1 |
| <a name="requirement_sentry"></a> [sentry](#requirement\_sentry) | 0.9.2 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.22.0 |
| <a name="provider_heroku"></a> [heroku](#provider\_heroku) | 5.1.0 |
| <a name="provider_mongodbatlas"></a> [mongodbatlas](#provider\_mongodbatlas) | 1.4.1 |
| <a name="provider_sentry"></a> [sentry](#provider\_sentry) | 0.9.2 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_s3_bucket.lhbot_reports_bucket](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket.lhcloudy_bot_config](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket.terraform_state_lhbot](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_policy.lhbot_bucket_policy](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket_policy) | resource |
| [aws_s3_bucket_public_access_block.lhbot_reports_bucket_public_access_block](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_public_access_block.lhcloudy_bot_config_public_access_block](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_public_access_block.terraform_state_lhbot_public_access_block](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.lhcloudy_bot_config_server_side_encryption](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.terraform_state_lhbot_server_side_encryption](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [heroku_app.lhbot](https://registry.terraform.io/providers/heroku/heroku/latest/docs/resources/app) | resource |
| [heroku_app_release.lhbot](https://registry.terraform.io/providers/heroku/heroku/latest/docs/resources/app_release) | resource |
| [heroku_app_webhook.lhbot](https://registry.terraform.io/providers/heroku/heroku/latest/docs/resources/app_webhook) | resource |
| [heroku_build.lhbot](https://registry.terraform.io/providers/heroku/heroku/latest/docs/resources/build) | resource |
| [heroku_collaborator.lhbot](https://registry.terraform.io/providers/heroku/heroku/latest/docs/resources/collaborator) | resource |
| [heroku_formation.lhbot](https://registry.terraform.io/providers/heroku/heroku/latest/docs/resources/formation) | resource |
| [heroku_slug.lhbot](https://registry.terraform.io/providers/heroku/heroku/latest/docs/resources/slug) | resource |
| [mongodbatlas_cluster.lhcloudy_cluster](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.4.1/docs/resources/cluster) | resource |
| [mongodbatlas_database_user.lhcloudybot_db_user](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.4.1/docs/resources/database_user) | resource |
| [sentry_project.sentry_lhcloudybot](https://registry.terraform.io/providers/jianyuan/sentry/0.9.2/docs/resources/project) | resource |
| [aws_iam_policy_document.lhbot_bucket_policy](https://registry.terraform.io/providers/hashicorp/aws/4.22.0/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app_name"></a> [app\_name](#input\_app\_name) | The name of the Heroku app | `string` | n/a | yes |
| <a name="input_app_quantity"></a> [app\_quantity](#input\_app\_quantity) | Number of dynos in your Heroku formation | `number` | `1` | no |
| <a name="input_app_region"></a> [app\_region](#input\_app\_region) | The region to deploy the app to | `string` | n/a | yes |
| <a name="input_app_version"></a> [app\_version](#input\_app\_version) | Version of the app | `string` | n/a | yes |
| <a name="input_aws_profile"></a> [aws\_profile](#input\_aws\_profile) | AWS profile to use | `string` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | AWS region to use | `string` | n/a | yes |
| <a name="input_collaborator_email"></a> [collaborator\_email](#input\_collaborator\_email) | Email of the collaborator | `string` | n/a | yes |
| <a name="input_database_password"></a> [database\_password](#input\_database\_password) | Mongodb Atlas database password | `string` | n/a | yes |
| <a name="input_database_user"></a> [database\_user](#input\_database\_user) | Mongodb Atlas database user | `string` | n/a | yes |
| <a name="input_dyno_size"></a> [dyno\_size](#input\_dyno\_size) | Size of dyno | `string` | n/a | yes |
| <a name="input_dyno_type"></a> [dyno\_type](#input\_dyno\_type) | Type of dyno | `string` | n/a | yes |
| <a name="input_heroku_api_key"></a> [heroku\_api\_key](#input\_heroku\_api\_key) | Heroku API Key | `string` | n/a | yes |
| <a name="input_heroku_email"></a> [heroku\_email](#input\_heroku\_email) | n/a | `string` | `"Heroku account email"` | no |
| <a name="input_heroku_enviorment_vars"></a> [heroku\_enviorment\_vars](#input\_heroku\_enviorment\_vars) | Environment variables for Heroku app | `map(string)` | n/a | yes |
| <a name="input_heroku_stack"></a> [heroku\_stack](#input\_heroku\_stack) | Stack for your Heroku app | `string` | n/a | yes |
| <a name="input_lh_bot_reports_s3_bucket"></a> [lh\_bot\_reports\_s3\_bucket](#input\_lh\_bot\_reports\_s3\_bucket) | S3 bucket for the reports | `string` | n/a | yes |
| <a name="input_lh_bot_s3_bot_config_bucket"></a> [lh\_bot\_s3\_bot\_config\_bucket](#input\_lh\_bot\_s3\_bot\_config\_bucket) | S3 bucket for the bot config | `string` | n/a | yes |
| <a name="input_lh_bot_s3_terraform_state_bucket"></a> [lh\_bot\_s3\_terraform\_state\_bucket](#input\_lh\_bot\_s3\_terraform\_state\_bucket) | S3 bucket for the terraform state | `string` | n/a | yes |
| <a name="input_mongo_auth_database_name"></a> [mongo\_auth\_database\_name](#input\_mongo\_auth\_database\_name) | Mongodb Atlas auth database name | `string` | n/a | yes |
| <a name="input_mongo_database_name"></a> [mongo\_database\_name](#input\_mongo\_database\_name) | Mongodb Atlas database name | `string` | n/a | yes |
| <a name="input_mongodb_cluster_name"></a> [mongodb\_cluster\_name](#input\_mongodb\_cluster\_name) | Mongodb Atlas cluster name | `string` | n/a | yes |
| <a name="input_mongodb_project_id"></a> [mongodb\_project\_id](#input\_mongodb\_project\_id) | Mongodb Atlas project ID | `string` | n/a | yes |
| <a name="input_mongodb_region"></a> [mongodb\_region](#input\_mongodb\_region) | Mongodb Atlas region | `string` | n/a | yes |
| <a name="input_mongodbatlas_private_key"></a> [mongodbatlas\_private\_key](#input\_mongodbatlas\_private\_key) | Mongodb Atlas private key | `string` | n/a | yes |
| <a name="input_mongodbatlas_public_key"></a> [mongodbatlas\_public\_key](#input\_mongodbatlas\_public\_key) | Mongodb Atlas public key | `string` | n/a | yes |
| <a name="input_sentry_organization"></a> [sentry\_organization](#input\_sentry\_organization) | Sentry organization | `string` | n/a | yes |
| <a name="input_sentry_project_name"></a> [sentry\_project\_name](#input\_sentry\_project\_name) | Sentry project name | `string` | n/a | yes |
| <a name="input_sentry_slug"></a> [sentry\_slug](#input\_sentry\_slug) | Sentry slug | `string` | n/a | yes |
| <a name="input_sentry_team_name"></a> [sentry\_team\_name](#input\_sentry\_team\_name) | Sentry team name | `string` | n/a | yes |
| <a name="input_sentry_token"></a> [sentry\_token](#input\_sentry\_token) | Sentry token | `string` | n/a | yes |
| <a name="input_source_code_url"></a> [source\_code\_url](#input\_source\_code\_url) | URL to the source code | `string` | n/a | yes |
| <a name="input_webhook_url"></a> [webhook\_url](#input\_webhook\_url) | URL to the webhook | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_app_name"></a> [app\_name](#output\_app\_name) | Application name |
| <a name="output_database_url"></a> [database\_url](#output\_database\_url) | Database URL |
| <a name="output_status"></a> [status](#output\_status) | Application status |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
