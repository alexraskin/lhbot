FROM python:3.10.2-slim-buster

LABEL MAINTAINER="alexraskin"

RUN pip install --upgrade pip

COPY ./ /

RUN pip install -r requirements.txt

HEALTHCHECK CMD discordhealthcheck || exit 1

CMD ["python3", "bot/bot.py"]