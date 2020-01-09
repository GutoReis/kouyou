# !/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from kouyou import __version__ as VERSION


with open("README.md") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()


setup(
    name="kouyou",
    version=VERSION,

    description="My personal utils project",
    long_description=readme + "\n\n" + history,
    author="Gustavo Reis",
    url="https://github.com/GutoReis/kouyou",
    packages=find_packages(),
    include_package_data=True,
    package_dir={"kouyou": "kouyou"},
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8"
    ]
)