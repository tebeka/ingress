#!/bin/bash

python setup.py sdist upload
python setup.py bdist_egg upload
python2 setup.py bdist_egg upload
