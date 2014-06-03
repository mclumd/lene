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

from lene.utils import *
from lene.exceptions import *
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
    def root(self):
        return (self.node, RDF.type, OWL.Class)

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

    def unbind(self, graph):
        """
        Remove the triples of this class from a particular graph
        """
        graph.remove((self.node, None, None))

    def isbound(self, graph):
        """
        Check if this type has been registered in the graph
        """
        return self.root in graph

    def instantiate(self, name, graph=None):
        """
        Returns a triple representing the instance of this class
        """
        instance = (URIRef(UMD[name]), RDF.type, self.node)
        if graph:
            graph.add(instance)
        return instance

class OWLGraph(object):
    """
    Wraps the rdflib graph object to create an OWL specific graph, notably
    from a Symbolic expression tree that is parsed from a lisp file.

    TODO: This is badly named and badly added in code- just here to make
        the development go faster. Some sort of decoupling from this object
        and the S-Expressions in Lisp is required.
    """

    # TODO: Replace with a regular expression
    DEFINES = ('define-frame', 'define-attribute-value', 'define-relation')

    def __init__(self, tree, lazy=False):
        """
        If lazy, do not run the make_graph method on the tree, but keep
        the graph object as None, this will ensure lazy loading is possible
        """
        self.graph = None
        self.tree  = tree
        if not lazy: self.make_graph()

    def make_graph(self):
        if self.graph is not None:
            raise GraphBindingError("Graph has already been created on %r" % self)
        self.graph = Graph()

        for stmt in self.tree:
            if stmt[0] in self.DEFINES:
                label = stmt[1].lower()
                props = stmt[2]

                if props[0].lower() == 'isa':
                    plabel = props[1][1][0].lower()
                    parent = OWLClass(plabel, OWL.Thing, plabel.title())
                    if not parent.isbound(self.graph):
                        parent.bind(self.graph)

                    if stmt[0] == 'define-attribute-value':
                        thing = parent.instantiate(label, graph=self.graph)
                    else:
                        thing  = OWLClass(label, parent.node, label.title())
                        if thing.isbound(self.graph):
                            thing.unbind(self.graph)
                        thing.bind(self.graph)

        return self.graph

    def serialize(self, *args, **kwargs):
        self.graph.bind("dc", DC)
        self.graph.bind("owl", OWL)
        self.graph.bind("umd", UMD)
        return self.graph.serialize(*args, **kwargs)

    def write(self, path):
        with open(path, 'w') as out:
            out.write(self.serialize())

    def __contains__(self, obj):
        return obj in self.graph

    def __iter__(self):
        for obj in self.graph:
            yield obj

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
