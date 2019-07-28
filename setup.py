# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='luigi_extension',
    version='0.0.1',
    description='luigi extention task classes.',
    long_description=readme,
    author='k1414st',
    author_email='k1414st@gmail.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['luigi'],
)

