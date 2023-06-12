#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


setup(
    packages=find_packages(include=['sobolanism', 'sobolanism.*']),
    test_suite='tests',
    zip_safe=False,
    setup_requires=["pbr>=2.0.0"],
    pbr=True,
)
