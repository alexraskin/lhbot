resource "discord_category_channel" "voice_chatting" {
  name      = "voice-chatting"
  server_id = discord_server.testing_server.id
  position  = 0
}

resource "discord_voice_channel" "general" {
  name      = "general"
  server_id = discord_server.testing_server.id
  position  = 0
  category  = discord_category_channel.voice_chatting.id
}
