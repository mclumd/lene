# lene.utils
# Utility functions and modules for lene
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 14:23:44 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: __init__.py [] bengfort@cs.umd.edu $

"""
Utility functions and modules for lene
"""

##########################################################################
## Imports
##########################################################################


##########################################################################
## Minor helper functions
##########################################################################

def number(numstr):
    """
    Attempts to parse a number from a string
    """
    try:
        return int(numstr)
    except ValueError:
        return float(numstr)
