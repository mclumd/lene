#!/usr/bin/env python
# setup
# Setup script for lene
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 08:53:47 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: setup.py [] bengfort@cs.umd.edu $

"""
Setup script for lene
"""

##########################################################################
## Imports
##########################################################################

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")

##########################################################################
## Package Information
##########################################################################

packages = find_packages(where=".", exclude=("tests", "scripts", "docs", "fixtures",))
requires = []

with open('requirements.txt', 'r') as reqfile:
    for line in reqfile:
        requires.append(line.strip())

classifiers = (
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Lisp',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Software Development :: Disassemblers',
    'Topic :: Text Processing :: General',
)

config = {
    "name": "META-Aqua Lene",
    "version": "0.2",
    "description": "A frame extraction tool for META-Aqua",
    "author": "Benjamin Bengfort",
    "author_email": "bengfort@cs.umd.edu",
    "url": "https://github.com/mclumd/lene/",
    "packages": packages,
    "install_requires": requires,
    "classifiers": classifiers,
    "zip_safe": True,
    "scripts": ["scripts/lene"],
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)
