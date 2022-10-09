# discord-server

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_discord"></a> [discord](#requirement\_discord) | 0.0.4 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_discord"></a> [discord](#provider\_discord) | 0.0.4 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [discord_category_channel.chatting](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/category_channel) | resource |
| [discord_category_channel.terraform_updates](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/category_channel) | resource |
| [discord_category_channel.voice_chatting](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/category_channel) | resource |
| [discord_invite.main_invite](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/invite) | resource |
| [discord_member_roles.memeber](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/member_roles) | resource |
| [discord_member_roles.moderator](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/member_roles) | resource |
| [discord_role.memeber](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/role) | resource |
| [discord_role.moderator](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/role) | resource |
| [discord_server.testing_server](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/server) | resource |
| [discord_text_channel.general](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/text_channel) | resource |
| [discord_text_channel.server_updates](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/text_channel) | resource |
| [discord_voice_channel.general](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/resources/voice_channel) | resource |
| [discord_color.blue](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/data-sources/color) | data source |
| [discord_color.green](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/data-sources/color) | data source |
| [discord_local_image.logo](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/data-sources/local_image) | data source |
| [discord_permission.member](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/data-sources/permission) | data source |
| [discord_permission.moderator](https://registry.terraform.io/providers/aequasi/discord/0.0.4/docs/data-sources/permission) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_discord_region"></a> [discord\_region](#input\_discord\_region) | Discord server region | `string` | n/a | yes |
| <a name="input_discord_server_name"></a> [discord\_server\_name](#input\_discord\_server\_name) | Discord server name | `string` | n/a | yes |
| <a name="input_discord_token"></a> [discord\_token](#input\_discord\_token) | Discord bot token | `string` | n/a | yes |
| <a name="input_members"></a> [members](#input\_members) | Members | `list(string)` | n/a | yes |
| <a name="input_moderators"></a> [moderators](#input\_moderators) | Moderators | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_invite_id"></a> [invite\_id](#output\_invite\_id) | n/a |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
