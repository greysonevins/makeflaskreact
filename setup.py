import os
from setuptools import setup

try:
    with open('requirements.txt') as f:
        required = f.read().splitlines()
except:
    required = []

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="makeflaskreact",
    version="0.0.1",
    author="Greyson Nevins-Archer",
    author_email="greyson.nevins@gmail.com",
    description="To make it easier to create a quick flask react app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greysonevins/makeflaskreact",
    license='MIT',
    packages=['makeflaskreact'],
    install_requires=required,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={"console_scripts": ["makeflaskreact=makeflaskreact.__init__:main"]},
)
