.PHONY: style
.PHONY: run
.PHONY: install
.PHONY: test
.PHONY: terraform-fmt
.PHONY: pre-commit

style:
	black .
	isort .

run:
	bash run.sh

terraform-fmt:
	terraform fmt -recursive

pre-commit:
	pre-commit run --all

export:
	pip freeze > requirements.txt