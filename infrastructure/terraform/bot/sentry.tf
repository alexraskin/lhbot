provider "sentry" {
  token = var.sentry_token
}

resource "sentry_project" "sentry_lhcloudybot" {
  organization = var.sentry_organization

  teams = [
    var.sentry_team_name,
  ]
  name = var.sentry_project_name
  slug = var.sentry_slug

  platform    = "python"
  resolve_age = 720
}
