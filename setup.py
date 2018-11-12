#!/usr/bin/env python

from setuptools import setup


def version():
    with open('ingress.py') as fp:
        for line in fp:
            if '__version__' not in line:
                continue
            _, ver = line.split('=')
            return ver.replace("'", '').strip()


with open('README.md') as fp:
    long_desc = fp.read()


setup(
    name='ingress',
    version=version(),
    description='A back door to servers.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    url='https://github.com/tebeka/ingress',
    license='MIT License',
    platforms=['any'],
    zip_safe=True,
    py_modules=['ingress'],
    install_requires=['six'],
    tests_require=['pytest', 'flake8'],
)
