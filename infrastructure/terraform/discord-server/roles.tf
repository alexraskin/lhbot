resource "discord_role" "moderator" {
  server_id   = discord_server.testing_server.id
  name        = "Moderator"
  permissions = data.discord_permission.moderator.allow_bits
  color       = data.discord_color.green.dec
  hoist       = true
  mentionable = true
  position    = 1
}

resource "discord_role" "memeber" {
  server_id   = discord_server.testing_server.id
  name        = "Testers"
  permissions = data.discord_permission.member.allow_bits
  color       = data.discord_color.blue.dec
  hoist       = true
  mentionable = true
  position    = 2
}

data "discord_color" "green" {
  rgb = "rgb(46, 204, 113)"
}

data "discord_color" "blue" {
  rgb = "rgb(52, 152, 219)"
}


data "discord_permission" "moderator" {
  kick_members          = "allow"
  ban_members           = "allow"
  manage_nicknames      = "allow"
  view_audit_log        = "allow"
  priority_speaker      = "allow"
  create_instant_invite = "allow"
  manage_roles          = "allow"
  administrator         = "allow"
  add_reactions         = "allow"
}

data "discord_permission" "member" {
  view_channel     = "allow"
  send_messages    = "allow"
  use_vad          = "deny"
  priority_speaker = "deny"
  change_nickname  = "allow"
}

resource "discord_member_roles" "moderator" {
  for_each  = toset(var.moderators)
  user_id   = each.key
  server_id = discord_server.testing_server.id
  role {
    role_id  = discord_role.moderator.id
    has_role = true
  }
}

resource "discord_member_roles" "memeber" {
  for_each  = toset(var.members)
  user_id   = each.key
  server_id = discord_server.testing_server.id
  role {
    role_id  = discord_role.memeber.id
    has_role = true
  }
  role {
    role_id  = discord_role.moderator.id
    has_role = false
  }
}