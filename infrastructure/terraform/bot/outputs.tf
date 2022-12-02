output "service_url" {
  value       = aws_apprunner_service.runner_service.service_url
  description = "The URL of the service"
}

output "database_url" {
  value       = "mongodb+srv://${var.database_user}:${var.database_password}@${split("//", mongodbatlas_cluster.lhcloudy_cluster.connection_strings.0.standard_srv)[1]}/${var.mongo_database_name}?retryWrites=true&w=majority"
  description = "Database URL"
}

output "app_name" {
  value       = heroku_app.lhbot.name
  description = "Application name"
}

output "status" {
  value       = heroku_build.lhbot.status
  description = "Application status"
}