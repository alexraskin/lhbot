## LhBot
___

<p align="center" width="50%">
    <img width="33%" src="https://i.gyazo.com/632f0e60dc0535128971887acad98993.png">
</p>

[Profile Picture Credit](https://twitter.com/PetraYle)

![GitHub](https://img.shields.io/github/license/alexraskin/lhbot)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)

---
#### Why did I make LhBot?
If you follow LhCloudy on twitch, you will know, that he will not share what Lh stands for in his name. I decided to write a discord bot, that keeps track of everyone's guesses in his discord, plus a bunch of other fun things. It is mainly used in his discord server, but you can also use it in your own server. Please create an issue if you have any questions.

---
#### Connect with LhCloudy
- [Twitch](https://www.twitch.tv/lhcloudy27)
- [Twitter](https://twitter.com/LhCloudy)
- [Discord](https://discord.com/invite/jd6CZSj8jb)
- [Youtube](https://www.youtube.com/channel/UC2CV-HWvIrMO4mUnYtNS-7A)

---
#### Deploy
This bot is completely managed by terraform and is deployed on AWS. If you are wanting to deploy this bot, you can do so by following the instructions below.

A few things you will need:
- Discord bot
- Mongo database (I use atlas)
- AWS Account
- Amazon S3 Bucket

Take a look in the `/example-files` folder for examples of the files you will need to create.

#### Deploying the bot to AWS via Terraform
1. Clone the repository
2. Change `dir` to `infrastructure/terraform/bot`
3. Create a `terraform.tfvars` The bot will look for all these environment variables [in this file](hhttps://github.com/alexraskin/lhbot/blob/main/infrastructure/terraform/bot/shared-envs.tf)
4. Run `terraform init`
5. Run `terraform apply --target aws_ecr_repository.ecr_repository`

- You will need to make sure the docker build is built and stored in the ECR repository. You can do this by running `docker build -t lhbot .` and then `docker tag lhbot:latest <aws_account_id>.dkr.ecr.eu-west-2.amazonaws.com/lhbot:latest` and then `docker push <aws_account_id>.dkr.ecr.eu-west-2.amazonaws.com/lhbot:latest` or something similar.

6. Run `terraform apply`

___
#### Run the bot locally
To run the bot locally, you will need to fill in the `.env` file all the values that are missing.
I prefer to use Docker to run the bot locally, but you may also use poetry to run the bot locally.

Docker
- `docker build -t lhbot:latest .`
- `docker run -it lhbot:latest` 

Poetry
- `make install`
- `make run`
___
#### Testing
We tried to make some tests for the bot. It is not perfect, but it is better than nothing.
- `make test`
