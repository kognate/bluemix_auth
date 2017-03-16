# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="bluemix_auth",
    version="0.1.0",
    description="package to wrap bluemix authentication (including openwhisk)",
    license="MIT",
    author="Joshua B. Smith",
    packages=find_packages(),
    install_requires=['requests'],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
    ]
)