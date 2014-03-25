#!/usr/bin/env python
# count
# Counts the tokens in a Lisp file
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Feb 27 11:04:30 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: count.py [] bengfort@cs.umd.edu $

"""
Counts the tokens in a Lisp file

TODO: test.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import json
import argparse
import operator

from lene import load
from lene.utils.stats import TokenFrequency

##########################################################################
## Main functionality
##########################################################################

def main(*argv):
    """
    Entry point for command functionality
    """

    config = {
        "description": "Counts the tokens at each level in a Lisp file.",
        "epilog": "Please report any errors to Ben."
    }
    parser = argparse.ArgumentParser(**config)
    parser.add_argument('-R', action="store_true", dest="recursively", help='Parse directory recursively')
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='?')
    namespace = parser.parse_args()

    tokens   = TokenFrequency.from_tree(load(namespace.infile))
    print tokens


if __name__ == '__main__':
    main(*sys.argv)
