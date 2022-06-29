.PHONY: style
.PHONY: run
.PHONY: install
.PHONY: test

style:
	black .
	isort .

run:
	poetry run bot/bot.py

test:
	cd tests
	poetry run pytest

install:
	poetry install

