resource "discord_category_channel" "terraform_updates" {
  name      = "server-updates"
  server_id = discord_server.testing_server.id
  position  = 0
}

resource "discord_text_channel" "server_updates" {
  name      = "updates"
  server_id = discord_server.testing_server.id
  position  = 0
  category  = discord_category_channel.terraform_updates.id
}

resource "discord_category_channel" "chatting" {
  name      = "text-chatting"
  server_id = discord_server.testing_server.id
  position  = 0
}

resource "discord_text_channel" "general" {
  name      = "general"
  server_id = discord_server.testing_server.id
  position  = 0
  category  = discord_category_channel.chatting.id
}
