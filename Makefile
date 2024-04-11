.PHONY: style
.PHONY: run
.PHONY: install
.PHONY: test

style:
	black .
	isort .

run:
	bash run.sh

export:
	pip3 freeze > requirements.txt