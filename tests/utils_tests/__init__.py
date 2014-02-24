# tests.utils_tests
# Testing of the utility functions in lene
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 14:31:29 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: __init__.py [] bengfort@cs.umd.edu $

"""
Testing of the utility functions in lene
"""

##########################################################################
## Imports
##########################################################################

import unittest
from lene.utils import *

##########################################################################
## Test Cases
##########################################################################

class UtilsTests(unittest.TestCase):

    def test_number_func(self):
        """
        Assert the number function parses ints and floats
        """
        self.assertTrue(isinstance(number('42'), int))
        self.assertTrue(isinstance(number('3.14'), float))
        with self.assertRaises(ValueError):
            number('abcd')

    def test_flatten_func(self):
        """
        Ensure that the flatten util works correctly.
        """
        tree = ['a', ['b', ['c', 'd'], 'e'], ['f', ['g', ['h'], ['i', ['j']]]]]
        flat = list(flatten(tree))
        self.assertEqual(flat, ['a','b','c','d','e','f','g','h','i','j'])
