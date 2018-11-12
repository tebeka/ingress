#!/usr/bin/env python

from setuptools import setup


def version():
    with open('ingress.py') as fp:
        for line in fp:
            if '__version__' not in line:
                continue
            _, ver = line.split('=')
            return ver.replace("'", '').strip()


setup(
    name='ingress',
    version=version(),
    description='A back door to servers.',
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    url='https://github.com/tebeka/ingress',
    license='MIT License',
    platforms=['any'],
    zip_safe=True,
    py_modules=['ingress'],
    install_requires=['six'],
)
