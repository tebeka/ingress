#!/usr/bin/env python

from setuptools import setup
import ingress

setup(
    name='ingress',
    version=ingress.__version__,
    description='A back door to servers.',
    long_description=ingress.__doc__,
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    url='https://bitbucket.org/tebeka/ingress/src',
    license='MIT License',
    platforms=['any'],
    zip_safe=True,
    py_modules=['ingress'],
    install_requires=['six'],
)

