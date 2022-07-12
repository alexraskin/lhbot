terraform {
  backend "s3" {
    bucket  = "discord-bot-testing-terraform-state"
    key     = "bot-testing/terraform.tfstate"
    encrypt = true
    region  = "us-east-1"
    profile = "discord-bot-testing"
  }
}

resource "discord_server" "testing_server" {
  name                          = var.discord_server_name
  region                        = var.discord_region
  default_message_notifications = 0
  icon_data_uri                 = data.discord_local_image.logo.data_uri
  verification_level            = 3
}

data "discord_local_image" "logo" {
  file = "logo.png"
}

resource "discord_invite" "main_invite" {
  channel_id = discord_text_channel.general.id
  max_age    = 0
}
