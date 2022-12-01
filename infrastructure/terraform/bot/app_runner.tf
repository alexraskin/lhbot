resource "aws_apprunner_service" "runner_service" {
  service_name                   = var.app_name
  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.runner_auto_scaling.arn
  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.runner_role.arn
    }
    auto_deployments_enabled = var.auto_deployments
    image_repository {
      #  make sure that you have the ecr module setup before hand
      image_identifier      = "${aws_ecr_repository.ecr_repository.repository_url}:latest"
      image_repository_type = "ECR"
      image_configuration {
        port                          = var.service_port
        runtime_environment_variables = var.enviorment_vars
      }
    }
  }
  instance_configuration {
    cpu    = var.service_cpu
    memory = var.service_memory
  }
  health_check_configuration {
    healthy_threshold   = var.service_healthy_threshold
    interval            = var.service_interval
    path                = var.service_health_check_path
    protocol            = var.protocol
    timeout             = var.timeout
    unhealthy_threshold = var.unhealthy_threshold
  }
  depends_on = [
    aws_iam_role_policy_attachment.runner_role_policy_attachment
  ]
}

resource "aws_apprunner_auto_scaling_configuration_version" "runner_auto_scaling" {
  auto_scaling_configuration_name = "${var.app_name}autoscaling"
  min_size                        = var.auto_scaling_min_size
  max_size                        = var.auto_scaling_max_size
}

resource "aws_apprunner_custom_domain_association" "lh_bot_domain" {
  domain_name = "lhbot.reinfrog.de"
  service_arn = aws_apprunner_service.runner_service.arn
}
