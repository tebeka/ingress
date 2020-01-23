all:
	$(error pick a target)

.PHONY: test
test:
	find . -name '*.pyc' -not -path '*/venv/*' -exec rm {} \;
	./venv/bin/python -m flake8 ingress.py test_ingress.py
	./venv/bin/python -m pytest -v test_ingress.py

.PHONY: upload-pypi
upload-pypi:
	-rm -f dist/ingress*
	./venv/bin/python setup.py sdist
	./venv/bin/python setup.py bdist_wheel
	./venv/bin/twine upload dist/*

venv:
	virtualenv venv
	./venv/bin/python -m pip install -r dev-requirements.txt


.PHONY: travis
travis:
	virtualenv venv
	./venv/bin/python -m pip install -r dev-requirements.txt
	$(MAKE) test
