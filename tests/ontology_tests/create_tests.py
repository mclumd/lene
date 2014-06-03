# tests.ontology_tests.create_tests
# Tests for the create functionality of the ontology
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  timestamp
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: create_tests.py [] benjamin@bengfort.com $

"""
Tests for the create functionality of the ontology.

This includes the construction of the following objects:

    * OWL Classes
    * OWL Data Properties
    * OWL Object Properties
    * OWL Instances

As well as the compilation, creation, and serialization of an entire
ontology to RDF/XML or to any other format supported by the lene package.
"""

##########################################################################
## Imports
##########################################################################

import unittest
import tempfile

from lene.exceptions import *
from lene.ontology.create import *
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DC, FOAF, OWL, RDF, RDFS

##########################################################################
## OWLClass Unit Tests
##########################################################################

class OWLClassTests(unittest.TestCase):

    @unittest.skip("Not implemented")
    def test_bind_to_graph(self):
        """
        Assert that binding adds correct number of nodes
        """
        pass

    @unittest.skip("Not implemented")
    def test_unbind_from_graph(self):
        """
        Assert that unbinding removes correct number of nodes
        """
        pass

##########################################################################
## OWLClass Integration Tests
##########################################################################

class OWLClassIntegrationTest(unittest.TestCase):
    """
    Test the complete construction of an OWL ontology with just simple
    OWL Class objects, etc.
    """

    def test_ontology_construction(self):
        """
        Test end to end ontology construction with OWLClass
        """

        # Create an RDF graph
        graph = Graph()

        # Create various classes
        Plant  = OWLClass("Plant", OWL.Thing, "The plant type", "The class of all plant types")
        Flower = OWLClass("Flower", UMD.Plant, "Flowering plants", "Flowering plants, also known as angiosperms.")
        Shrub  = OWLClass("Shrub", UMD.Plant, "Shrubbery", "Shrubs, a type of plant which branches from the base.")

        # Bind the classes to the graph
        Plant.bind(graph)
        Flower.bind(graph)
        Shrub.bind(graph)

        # Create and bind an instance of a flower
        instance = Flower.instantiate("Magnolia")
        graph.add(instance)

        self.assertIn(Plant.root, graph)
        self.assertIn(Flower.root, graph)
        self.assertIn(Shrub.root, graph)
        self.assertIn(instance, graph)

##########################################################################
## OWLGraph Tests
##########################################################################

class OWLGraphTests(unittest.TestCase):
    pass
