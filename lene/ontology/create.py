# lene.ontology.create
# Tools and helpers to create ontologies from scratch
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Jun 03 08:38:20 2014 -0400
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: create.py [] benjamin@bengfort.com $

"""
Tools and helpers to create ontologies from scratch
"""

##########################################################################
## Imports
##########################################################################

import logging

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DC, FOAF, OWL, RDF, RDFS

##########################################################################
## Module level code
##########################################################################

logging.basicConfig()                           # Configure Logging
UMD = Namespace("http://cs.umd.edu/active/#")    # Create UMD Namespace

##########################################################################
## OWL Class Constructor
##########################################################################

class OWLClass(object):
    """
    Construct an OWL Class
    """

    def __init__(self, name, parent, label="", comment=""):
        self.node    = URIRef(UMD[name])
        self.parent  = parent
        self.label   = label
        self.comment = comment

    @property
    def triples(self):
        """
        Returns the various triples constructed by this object.
        """
        return (
            (self.node, RDF.type, OWL.Class),
            (self.node, RDFS.subClassOf, self.parent),
            (self.node, RDFS.label, Literal(self.label)),
            (self.node, RDFS.comment, Literal(self.comment)),
        )

    def bind(self, graph):
        """
        Bind this class to a particular graph
        """
        for triple in self.triples:
            graph.add(triple)

    def instantiate(self, name):
        """
        Returns a triple representing the instance of this class
        """
        return (URIRef(UMD[name]), RDF.type, self.node)

##########################################################################
## Main method, usage, and testing
##########################################################################

if __name__ == '__main__':

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
    graph.add(Flower.instantiate("Magnolia"))

    # Bind the namespaces to the graph
    graph.bind("dc", DC)
    graph.bind("owl", OWL)
    graph.bind("umd", UMD)
    print graph.serialize()
