# test.parser_tests
# Tests for the parser module
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 14:43:17 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: __init__.py [] bengfort@cs.umd.edu $

"""
Tests for the parser module
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest
import tempfile

from lene.parser import *
from .tokenize_tests import simple_fixture

class ParserModuleTests(unittest.TestCase):

    def setUp(self):
        """
        Setup temporary file as fixture.
        """
        hndl, path = tempfile.mkstemp(suffix='.lisp', prefix='representation-')
        self.temppath = path
        with open(path, 'w') as lispy:
            lispy.write(simple_fixture)

    def tearDown(self):
        """
        Ensure removal of tempfile
        """
        if os.path.exists(self.temppath):
            os.remove(self.temppath)
        self.assertFalse(os.path.exists(self.temppath))

    def test_load(self):
        """
        Test the load function

        TODO: Test with various options
        """
        tree = load(self.temppath)
        self.assertTrue(tree)

    def test_loads(self):
        """
        Test the loads function

        TODO: Test with various options
        """
        tree = loads(simple_fixture)
        self.assertTrue(tree)

    def test_load_token_tree(self):
        """
        Test loading a token tree with load

        TODO: Check to ensure there are tokens in the tree
        """
        tree = load(self.temppath, detokenize=False)
        self.assertTrue(tree)
