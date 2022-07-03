## LhBot

<p align="center" width="50%">
    <img width="33%" src="https://i.gyazo.com/632f0e60dc0535128971887acad98993.png">
</p>

PFP Credit: https://twitter.com/PetraYle

![GitHub](https://img.shields.io/github/license/alexraskin/lhbot)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)

---
### What is LhBot?
If you follow LhCloudy on twitch, you will know that he will not share what Lh stands for in his name. I decided to write a discord bot that keeps track of everyone's guesses in his discord, plus a bunch of other fun things. It is mainly used in his discord server, but you can also use it in your own server.

---
### Connect with LhCloudy
[Twitch](https://www.twitch.tv/lhcloudy27)
[Twitter](https://twitter.com/LhCloudy)
[Discord](https://discord.com/invite/jd6CZSj8jb)
[Youtube](https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A)

---
### Deploy
This bot is completely managed by terraform and is deployed on heroku. If you are wanting to deploy this bot, you can do so by following the instructions below.

A few things you will need:
- Mongo database 
- Discord bot
- Heroku App
- Amazon S3 Bucket

Take a look in the `/example-files` folder for more information.

The bot will look for all these environment variables [in this file](https://github.com/alexraskin/lhbot/blob/main/infrastructure/terraform/shared-envs.tf)

1. Clone the repository
2. Change `dir` to `infrastructure/terraform`
3. Create a `terraform.tfvars` file
4. Run `terraform init`
5. Run `terraform apply`

___
### Run the bot locally
To run the bot locally, you will need to fill in the `.env` file all the values that are missing.

I prefer to use Docker to run the bot locally, but you may also use poetry to run the bot locally.

Docker
- `docker build -t lhbot:latest .`
- `docker run -it lhbot:latest` 

Poetry
- `poetry install`
- `poetry run bot/bot.py`
___
### Testing
We tried to make some tests for the bot. It is not perfect, but it is better than nothing.
- `cd tests`  
  
- `poetry run pytest`
___
