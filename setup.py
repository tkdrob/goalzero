#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goalzero",
    version="master",
    author="Robert Hillis",
    author_email="tkdrob4390@yahoo.com",
    description="Goal Zero REST Api Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tkdrob/goalzero",
    packages=setuptools.find_packages(),
    install_requires=['aiohttp>=3.4.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
