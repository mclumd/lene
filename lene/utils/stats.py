# lene.utils.stats
# Provides a statistical analysis of tokens
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Feb 27 10:58:35 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: stats.py [] bengfort@cs.umd.edu $

"""
Provides a statistical analysis of tokens
"""

##########################################################################
## Imports
##########################################################################

from collections import defaultdict

##########################################################################
## Evaluation Classes
##########################################################################

class TokenFrequency(object):
    """
    Evaluates the frequency of tokens at each depth of a Tree
    """

    def __init__(self, tree):
        self.tree = tree

    def walk(self, tree=None, depth=0):
        """
        Walks the tree, producing the discovered tokens and their depth.
        """
        tree = tree or self.tree
        for idx,node in enumerate(tree):
            if isinstance(node, list):
                for idx, subnode, nextdepth in self.walk(node, depth+1):
                    yield idx, subnode, nextdepth
            else:
                yield idx, node, depth

    def count(self):
        tokens = defaultdict(lambda: defaultdict(int))
        for idx, token, depth in self.walk():
            if idx > 0: continue
            tokens[depth][token] += 1
        return tokens
