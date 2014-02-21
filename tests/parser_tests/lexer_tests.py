# tests.parser_tests.lexer_tests
# Tests for the lexical analysis module for lene
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 15:51:24 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: lexer_tests.py [] bengfort@cs.umd.edu $

"""
Tests for the lexical analysis module for lene
"""

##########################################################################
## Imports
##########################################################################

import unittest

from lene.parser.lexer import *
from tokenize_tests import fixture
from lene.parser.tokenize import Tokenizer

##########################################################################
## Test Cases
##########################################################################

class LexerTests(unittest.TestCase):
    """
    Tests the lexer module with a token stream
    """

    def setUp(self):
        self.tokens = Tokenizer().tokenize(fixture)

    def tearDown(self):
        self.tokens = None

