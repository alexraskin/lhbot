output "app_url" {
  value       = heroku_app.lhbot.web_url
  description = "Application URL"
}

output "app_name" {
  value       = heroku_app.lhbot.name
  description = "Application name"
}

output "app_region" {
  value       = heroku_app.lhbot.region
  description = "Application region"
}

output "app_stack" {
  value       = heroku_app.lhbot.stack
  description = "Application stack"
}
