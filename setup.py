import os
from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="makeflaskreact",
    version="1.0.7",
    author="Greyson Nevins-Archer",
    author_email="greyson.nevins@gmail.com",
    description="To make it easier to create a quick flask react app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greysonevins/makeflaskreact",
    license='MIT',
    packages=['makeflaskreact'],
    include_package_data=True,
    install_requires=[
            "click",
            "virtualenv",
            'click-spinner'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={"console_scripts": ["reactflask=makeflaskreact.__init__:main"]},
)
