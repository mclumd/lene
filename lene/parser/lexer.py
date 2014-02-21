# lene.parser.lexer
# Lexical analysis for Lene module
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 15:51:24 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: lexer.py [] bengfort@cs.umd.edu $

"""
Lexical analysis for Lene module
"""

##########################################################################
## Imports
##########################################################################

from .tokenize import *

##########################################################################
## Lexer Class
##########################################################################

class Lexer(object):
    """
    Takes as input an iterable of tokens and returns a Python data
    structure capable of representing complex Lisp structures and frames.
    """

    def __init__(self, tokens):
        self.tokens = tokens
