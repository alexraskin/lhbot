variable "discord_token" {
  description = "Discord bot token"
  type        = string
}

variable "discord_server_name" {
  description = "Discord server name"
  type        = string
}

variable "discord_region" {
  description = "Discord server region"
  type        = string
}

variable "moderators" {
  description = "Moderators"
  type        = list(string)
}

variable "members" {
  description = "Members"
  type        = list(string)
}
