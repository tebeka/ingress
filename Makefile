all:
	$(error pick a target)

test:
	find . -name '*.pyc' -exec rm {} \;
	pipenv run flake8 ingress.py test_ingress.py
	pipenv run python -m pytest -v test_ingress.py

upload-pypi:
	-rm -f dist/ingress*
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

travis:
	pip install pipenv
	pipenv sync --dev
	$(MAKE) test
