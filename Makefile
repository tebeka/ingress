.PHONY: all test publish upload-pypi

all:
	$(error pick a target)

test:
	uv run ruff check ingress.py test/test_ingress.py
	uv run bandit ingress.py
	uv run python -m pytest -v test/test_ingress.py

# Usage: make publish PART=minor (patch, minor or major)
PART ?= patch
publish: test
	uvx bump-my-version bump $(PART)
	git push --follow-tags

upload-pypi:
	uv publish
