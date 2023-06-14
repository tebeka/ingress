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
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Terminals :: Telnet',
    ],
    python_requires='>=3.9',
    keywords='shell telnet debug server',
)
