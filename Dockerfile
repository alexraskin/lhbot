FROM python:3.10.5-slim-buster

LABEL MAINTAINER="alexraskin"

RUN pip install --upgrade pip

COPY ./ /

RUN pip install -r requirements.txt

CMD ["python3", "bot/bot.py"]