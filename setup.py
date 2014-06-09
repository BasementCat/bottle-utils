#!/usr/bin/env python
import os
from setuptools import setup

def read(filen):
    with open(os.path.join(os.path.dirname(__file__), filen), "r") as fp:
        return fp.read()
 
config = dict(
    name                = "bottleutils",
    version             = "0.1",
    description         = "Reusable components for bottle",
    long_description    = read("README.md"),
    author              = "Alec Elton",
    author_email        = "alec.elton@gmail.com",
    url                 = "https://github.com/BasementCat/bottle-utils",
    packages            = ["bottleutils"],
    install_requires    = ["bottle"],
    test_suite          = "nose.collector",
    tests_require       = ["nose", "sqlalchemy"],
)

if __name__ == "__main__":
    setup(**config)