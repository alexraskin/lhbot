# bot

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 4.42 |
| <a name="requirement_github"></a> [github](#requirement\_github) | ~> 5.3.0 |
| <a name="requirement_mongodbatlas"></a> [mongodbatlas](#requirement\_mongodbatlas) | ~> 1.6 |
| <a name="requirement_sentry"></a> [sentry](#requirement\_sentry) | ~> 0.9 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 4.44.0 |
| <a name="provider_github"></a> [github](#provider\_github) | 5.3.0 |
| <a name="provider_mongodbatlas"></a> [mongodbatlas](#provider\_mongodbatlas) | 1.6.0 |
| <a name="provider_sentry"></a> [sentry](#provider\_sentry) | 0.10.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_apprunner_auto_scaling_configuration_version.runner_auto_scaling](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/apprunner_auto_scaling_configuration_version) | resource |
| [aws_apprunner_custom_domain_association.lh_bot_domain](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/apprunner_custom_domain_association) | resource |
| [aws_apprunner_service.runner_service](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/apprunner_service) | resource |
| [aws_ecr_lifecycle_policy.ecr_lifecycle_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_lifecycle_policy) | resource |
| [aws_ecr_repository.ecr_repository](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecr_repository) | resource |
| [aws_iam_role.runner_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.runner_role_policy_attachment](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_s3_bucket.lhbot_reports_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket.lhcloudy_bot_config](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket.terraform_state_lhbot](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket) | resource |
| [aws_s3_bucket_policy.lhbot_bucket_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_policy) | resource |
| [aws_s3_bucket_public_access_block.lhbot_reports_bucket_public_access_block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_public_access_block.lhcloudy_bot_config_public_access_block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_public_access_block.terraform_state_lhbot_public_access_block](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_public_access_block) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.lhcloudy_bot_config_server_side_encryption](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [aws_s3_bucket_server_side_encryption_configuration.terraform_state_lhbot_server_side_encryption](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket_server_side_encryption_configuration) | resource |
| [github_actions_secret.aws_ac_key](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/actions_secret) | resource |
| [github_actions_secret.aws_ecr_repo](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/actions_secret) | resource |
| [github_actions_secret.aws_s_key](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/actions_secret) | resource |
| [github_actions_secret.lhbot_github_actions_secret](https://registry.terraform.io/providers/integrations/github/latest/docs/resources/actions_secret) | resource |
| [mongodbatlas_cluster.lhcloudy_cluster](https://registry.terraform.io/providers/mongodb/mongodbatlas/latest/docs/resources/cluster) | resource |
| [mongodbatlas_database_user.lhcloudybot_db_user](https://registry.terraform.io/providers/mongodb/mongodbatlas/latest/docs/resources/database_user) | resource |
| [sentry_project.sentry_lhcloudybot](https://registry.terraform.io/providers/jianyuan/sentry/latest/docs/resources/project) | resource |
| [aws_iam_policy_document.lhbot_bucket_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app_name"></a> [app\_name](#input\_app\_name) | The name of the Heroku app | `string` | n/a | yes |
| <a name="input_auto_deployments"></a> [auto\_deployments](#input\_auto\_deployments) | Whether or not to automatically deploy new code to the service. Defaults to true | `bool` | `true` | no |
| <a name="input_auto_scaling_max_size"></a> [auto\_scaling\_max\_size](#input\_auto\_scaling\_max\_size) | The maximum number of instances to run for the service. Defaults to 5. Minimum value of 1. Maximum value of 25 | `number` | `5` | no |
| <a name="input_auto_scaling_min_size"></a> [auto\_scaling\_min\_size](#input\_auto\_scaling\_min\_size) | The minimum number of instances to run for the service. Defaults to 1. Minimum value of 1. Maximum value of 25 | `number` | `1` | no |
| <a name="input_aws_profile"></a> [aws\_profile](#input\_aws\_profile) | AWS profile to use | `string` | n/a | yes |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | AWS region to use | `string` | n/a | yes |
| <a name="input_database_password"></a> [database\_password](#input\_database\_password) | Mongodb Atlas database password | `string` | n/a | yes |
| <a name="input_database_user"></a> [database\_user](#input\_database\_user) | Mongodb Atlas database user | `string` | n/a | yes |
| <a name="input_docker_image_tag"></a> [docker\_image\_tag](#input\_docker\_image\_tag) | Which ECR Image tag to use | `string` | `"latest"` | no |
| <a name="input_enviorment_vars"></a> [enviorment\_vars](#input\_enviorment\_vars) | Environment variables for the app | `map(string)` | n/a | yes |
| <a name="input_github_token"></a> [github\_token](#input\_github\_token) | Github token | `string` | n/a | yes |
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
| <a name="input_protocol"></a> [protocol](#input\_protocol) | The IP protocol that App Runner uses to perform health checks for your service. Valid values: TCP, HTTP. Defaults to TCP. If you set protocol to HTTP, App Runner sends health check requests to the HTTP path specified by path. | `string` | `"TCP"` | no |
| <a name="input_sentry_organization"></a> [sentry\_organization](#input\_sentry\_organization) | Sentry organization | `string` | n/a | yes |
| <a name="input_sentry_project_name"></a> [sentry\_project\_name](#input\_sentry\_project\_name) | Sentry project name | `string` | n/a | yes |
| <a name="input_sentry_slug"></a> [sentry\_slug](#input\_sentry\_slug) | Sentry slug | `string` | n/a | yes |
| <a name="input_sentry_team_name"></a> [sentry\_team\_name](#input\_sentry\_team\_name) | Sentry team name | `string` | n/a | yes |
| <a name="input_sentry_token"></a> [sentry\_token](#input\_sentry\_token) | Sentry token | `string` | n/a | yes |
| <a name="input_service_cpu"></a> [service\_cpu](#input\_service\_cpu) | The number of cpu's to allocate to the service | `number` | `1024` | no |
| <a name="input_service_health_check_path"></a> [service\_health\_check\_path](#input\_service\_health\_check\_path) | The URL to send requests to for health checks. Defaults to /. Minimum length of 0. Maximum length of 51200. | `string` | `"/"` | no |
| <a name="input_service_healthy_threshold"></a> [service\_healthy\_threshold](#input\_service\_healthy\_threshold) | The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Defaults to 5. Minimum value of 1. Maximum value of 20. | `number` | `5` | no |
| <a name="input_service_interval"></a> [service\_interval](#input\_service\_interval) | The time interval, in seconds, between health checks. Defaults to 5. Minimum value of 1. Maximum value of 20. | `number` | `5` | no |
| <a name="input_service_memory"></a> [service\_memory](#input\_service\_memory) | The amount of memory to allocate to the service | `number` | `2048` | no |
| <a name="input_service_port"></a> [service\_port](#input\_service\_port) | n/a | `string` | `8000` | no |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | The time, in seconds, to wait for a health check response before deciding it failed. Defaults to 2. Minimum value of 1. Maximum value of 20. | `number` | `2` | no |
| <a name="input_unhealthy_threshold"></a> [unhealthy\_threshold](#input\_unhealthy\_threshold) | The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Defaults to 5. Minimum value of 1. Maximum value of 20. | `number` | `5` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_database_url"></a> [database\_url](#output\_database\_url) | Database URL |
| <a name="output_service_url"></a> [service\_url](#output\_service\_url) | The URL of the service |
| <a name="output_status"></a> [status](#output\_status) | The status of the service |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
