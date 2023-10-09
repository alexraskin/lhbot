provider "railway" {
  token = var.railway_token
}

resource "railway_project" "lhbot_project" {
  name        = "LhBot-Discord"
  description = "Discord Bot used in LhCloudys Discord"
}

resource "railway_service" "lhbot_service" {
  name       = "LhBot"
  project_id = railway_project.lhbot_project.id
}

resource "railway_environment" "lhbot_environment" {
  name       = "production"
  project_id = railway_project.lhbot_project.id
}

resource "railway_custom_domain" "lhbot_domain" {
  domain         = "lhbot.twizy.dev"
  environment_id = railway_environment.lhbot_environment.id
  service_id     = railway_service.lhbot_service.id
}

resource "railway_deployment_trigger" "lhbot_trigger" {
  repository     = "alexraskin/lhbot"
  branch         = "main"
  check_suites   = false
  environment_id = railway_environment.lhbot_environment.id
  service_id     = railway_service.lhbot_service.id
}

resource "railway_variable" "lhbot_vars" {
  for_each       = var.enviorment_vars
  name           = each.key
  value          = each.value
  environment_id = railway_environment.lhbot_environment.id
  service_id     = railway_service.lhbot_service.id
}
