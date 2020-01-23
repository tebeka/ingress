all:
	$(error pick a target)

test:
	find . -name '*.pyc' -exec rm {} \;
	python -m flake8 ingress.py test_ingress.py
	python -m pytest -v test_ingress.py

upload-pypi:
	-rm -f dist/ingress*
	python setup.py sdist
	python setup.py bdist_wheel
	twine upload dist/*

travis:
	python -m pip install -r dev-requirements.txt
	$(MAKE) test
