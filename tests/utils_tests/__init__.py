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

    def test_walk_func(self):
        """
        Ensure that the walk util works depth first

        Expected- an enumeration with idx, node, depth
        """
        tree = ['a', ['b', ['c', 'd'], 'e'], ['f', ['g', ['h'], ['i', ['j']]]]]
        flat = list(walk(tree))
        true = [(0, 'a', 0), (0, 'b', 1), (0, 'c', 2), (1, 'd', 2),
                (2, 'e', 1), (0, 'f', 1), (0, 'g', 2), (0, 'h', 3),
                (0, 'i', 3), (0, 'j', 4)]
        self.assertEqual(flat, true)
