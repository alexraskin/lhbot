# LhBot

[![LhBot](https://i.gyazo.com/632f0e60dc0535128971887acad98993.png)](https://twitter.com/PetraYle)

![Discord](https://img.shields.io/discord/766217366568304660)
[![Twitch Status](https://img.shields.io/twitch/status/lhcloudy27?color=6441a5&logo=twitch&logoColor=white)](https://www.twitch.tv/lhcloudy27)
[![Twitter Follow](https://img.shields.io/twitter/follow/lhcloudy?color=1DA1F2&logo=twitter&style=flat-square)](https://twitter.com/LhCloudy)
![GitHub](https://img.shields.io/github/license/alexraskin/lhbot?color=blue)

## Why did I make LhBot?

If you follow LhCloudy on twitch, you will know, that he will not share what Lh stands for in his name. I decided to write a discord bot, that keeps track of everyone's guesses in his discord, plus a bunch of other fun things. It is mainly used in his discord server, but you can also use it in your own server. Please create an issue if you have any questions.

## Connect with LhCloudy

- [Twitch](https://www.twitch.tv/lhcloudy27)
- [Twitter](https://twitter.com/LhCloudy)
- [Discord](https://discord.com/invite/jd6CZSj8jb)
- [Youtube](https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A)

## Deploy

This bot is completely managed by terraform and is deployed on [Railway](https://railway.app/). If you are wanting to deploy this bot, you can do so by following the instructions below.

A few things you will need:

- Discord bot
- Mongo database (I use atlas)
- A Railway account
- Amazon S3 Bucket

Take a look in the [`/example-files`](https://github.com/alexraskin/lhbot/tree/main/example-files) folder for examples of the files you will need to create.

## Deploying the bot to Railway via Terraform

1. Clone the repository
2. Change `dir` to `infrastructure/terraform/bot`
3. Create a `terraform.tfvars` The bot will look for all these environment variables [in this file](hhttps://github.com/alexraskin/lhbot/blob/main/infrastructure/terraform/bot/shared-envs.tf)
4. Run `terraform init`
5. Run `terraform apply`

___
## Run the bot locally

To run the bot locally, you will need to fill in the `.env` file all the values that are missing.

```bash
make run
```

## Contributing

If you would like to contribute to this project, please create an issue and we can discuss it there. I am open to any suggestions.
