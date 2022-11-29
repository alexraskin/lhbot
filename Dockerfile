FROM python:3.10.8-slim-buster

LABEL MAINTAINER="alexraskin"

WORKDIR /bot

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

COPY ./bot /bot

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

CMD ["python3", "bot/bot.py"]