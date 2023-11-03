all:
	$(error pick a target)

test:
	find . -name '*.pyc' -exec rm {} \;
	python -m ruff ingress.py test_ingress.py
	bandit ingress.py
	python -m pytest -v test_ingress.py

upload-pypi:
	-rm -f dist/ingress*
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload --config-file=.pypirc dist/*
