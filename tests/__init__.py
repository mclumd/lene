# tests
# Testing for the Lene package
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 08:44:14 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: __init__.py [] bengfort@cs.umd.edu $

"""
Testing for the Lene package
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest

##########################################################################
## Test Cases
##########################################################################

class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Test a simple world fact
        """
        self.assertEqual(2**3, 8)

    def test_import(self):
        """
        Assert our package can be imported
        """
        try:
            import lene
        except ImportError:
            self.fail("Unable to import lene module!")

    def test_membership(self):
        """
        Check top level module membership
        """
        import lene
        self.assertTrue(hasattr(lene, 'load'))
        self.assertTrue(hasattr(lene, 'loads'))
