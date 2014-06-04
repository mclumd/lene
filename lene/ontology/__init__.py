# lene.ontology
# Module for interacting with and accessing Ontologies
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Jun 03 10:09:22 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Module for interacting with and accessing Ontologies
"""

##########################################################################
## Imports
##########################################################################

from .base import *
from .create import OWLClass, OWLGraph, UMD

##########################################################################
## Module functions
##########################################################################

def make_graph(tree, lazy=False, **options):
    """
    Returns an RDF graph from a parsed LISP tree. Lazy loading means that
    you will have to call the `OWLGraph.make_graph` method yourself to get
    access to the RDF graph under the hood. Possible options are:

        - title
        - description
        - creators (a list of creators names)
        - date (defaults to the current date)

    This function doesn't do too much, but is a quick way to start making
    RDF graphs from S-Expression trees.
    """
    return OWLGraph(tree, lazy=lazy, **options)
