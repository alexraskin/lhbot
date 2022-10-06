.PHONY: style
.PHONY: run
.PHONY: install
.PHONY: test
.PHONY: terraform-fmt

style:
	black .
	isort .

run:
	poetry run python bot/bot.py

test:
	cd tests
	poetry run pytest

install:
	poetry install

terraform-fmt:
	terraform fmt -recursive
