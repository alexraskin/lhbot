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

output "release_id" {
  value       = heroku_app_release.lhbot.id
  description = "Release ID"
}

output "status" {
  value       = heroku_build.lhbot.status
  description = "Application status"
}

output "cluster_connection_sting" {
    value = split("//", mongodbatlas_cluster.lhcloudy_cluster.connection_strings.0.standard_srv)[1]
}
