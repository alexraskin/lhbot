FROM python:3.10-slim-buster

LABEL MAINTAINER="alexraskin"

RUN pip install pipenv

COPY ./ /

RUN pipenv install --system --deploy

CMD ["python3", "bot.py"]