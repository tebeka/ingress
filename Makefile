all:
	$(error pick a target)

test:
	uv run ruff check ingress.py test_ingress.py
	uv run bandit ingress.py
	uv run python -m pytest -v test_ingress.py

upload-pypi:
	uv publish
