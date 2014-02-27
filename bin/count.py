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

def main():
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

    freq   = TokenFrequency(load(namespace.infile))
    tokens = freq.count()
    for key in tokens:
        tokens[key] = sorted(tokens[key].items(), key=operator.itemgetter(1), reverse=True)

    for depth, counts in tokens.items():
        header = "Tree Level %i" % depth
        print header
        print "=" * len(header)
        for token, count in counts:
            print "  {0: <4} {1}".format(count, token)
        print

if __name__ == '__main__':
    main()
