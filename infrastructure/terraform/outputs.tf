output "app_name" {
  value       = heroku_app.lhbot.name
  description = "Application name"
}

output "status" {
  value       = heroku_build.lhbot.status
  description = "Application status"
}
