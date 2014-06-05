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
from datetime import datetime
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DC, FOAF, OWL, RDF, RDFS

##########################################################################
## Module level code
##########################################################################

logging.basicConfig()                               # Configure Logging
UMD = Namespace("http://cs.umd.edu/active/#")       # Create UMD Namespace

DEFINE                 = "define"                   # Standard define
DEFINE_FRAME           = "define-frame"             # Define a Thing
DEFINE_RELATION        = "define-relation"          # Define a Relation
DEFINE_ATTRIBUTE_VALUE = "define-attribute-value"   # Define an instance

XML_DATE               = "%b %d, %Y %H:%M:%S %p"

##########################################################################
## OWL Class Constructor
##########################################################################

class OWLClass(object):
    """
    Construct an OWL Class
    """

    def __init__(self, name, parent=OWL.Thing, label="", comment=""):
        self.node    = URIRef(UMD[name])
        self.parent  = parent.node if isinstance(parent, OWLClass) else parent
        self.label   = label or name
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
            self.root,
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
        return self

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

##########################################################################
## OWL Object Properties
##########################################################################

class OWLObjectProperty(OWLClass):
    """
    Helper to construct an OWL Object Property
    """

    def __init__(self, name, parent=OWL.topObjectProperty, domain=OWL.Thing,
                       range=OWL.Thing, label="", comment=""):

        self.node    = URIRef(UMD[name])
        self.parent  = parent.node if isinstance(parent, OWLClass) else parent
        self.domain  = domain.node if isinstance(domain, OWLClass) else domain
        self.range   = range.node if isinstance(range, OWLClass) else range
        self.label   = label or name
        self.comment = comment

    @property
    def root(self):
        return (self.node, RDF.type, OWL.ObjectProperty)

    @property
    def triples(self):
        """
        Returns the various triples constructed by this object.
        """
        return (
            self.root,
            (self.node, RDFS.subClassOf, self.parent),
            (self.node, OWL.domain, self.domain),
            (self.node, OWL.range, self.range),
            (self.node, RDFS.label, Literal(self.label)),
            (self.node, RDFS.comment, Literal(self.comment)),
        )

    def instantiate(self, domain, range, graph=None):
        domain   = domain[0] if isinstance(domain, tuple) else domain
        range    = range[0] if isinstance(range, tuple) else range

        instance = (domain, self.node, range)
        if graph:
            graph.add(instance)
        return instance

##########################################################################
## OWL Graph
##########################################################################

class OWLGraph(object):
    """
    Wraps the rdflib graph object to create an OWL specific graph, notably
    from a Symbolic expression tree that is parsed from a lisp file.

    TODO: This is badly named and badly added in code- just here to make
        the development go faster. Some sort of decoupling from this object
        and the S-Expressions in Lisp is required.
    """

    # TODO: Replace with a regular expression
    DEFINES = (DEFINE_FRAME, DEFINE_RELATION, DEFINE_ATTRIBUTE_VALUE)

    def __init__(self, tree, lazy=False, **opts):
        """
        If lazy, do not run the make_graph method on the tree, but keep
        the graph object as None, this will ensure lazy loading is possible
        """
        self.graph = None
        self.tree  = tree
        self.opts  = opts
        if not lazy: self.make_graph()

    def make_graph(self):
        """
        Construct the wrapped rdflib.Graph object along with defaults and
        read in the tree that was passed at instantiation to add to graph.
        """
        if self.graph is not None:
            raise GraphBindingError("Graph has already been created on %r" % self)
        self.graph = Graph()

        self.add_header()
        self.add_defaults()

        for stmt in self.tree:
            if stmt[0] in self.DEFINES:
                if stmt[0] == DEFINE_RELATION:
                    relation = self.add_relation(stmt)
                else:
                    thing = self.add_thing(stmt)
            else:
                logging.warn("Unknown expression '%s'" % stmt[0])
        return self.graph

    def add_header(self, **opts):
        """
        Constructs the owl:Ontology header if a title, description,
        creator, or date attributes have been passed in as opts. If so,
        it will also generate a description of the creation process.

        :note: creators should be a list of strings
        """
        self.opts.update(opts)

        title       = self.opts.get('title', '')
        description = self.opts.get('description', '')
        creators    = self.opts.get('creators', [])
        date        = self.opts.get('date', datetime.now().strftime(XML_DATE))
        header      = URIRef("http://cs.umd.edu/active/")

        self.graph.add((header, RDF.type, OWL.Ontology))
        self.graph.add((header, DC.title, Literal(title)))
        self.graph.add((header, DC.description, Literal(description)))
        self.graph.add((header, DC.date, Literal(date)))

        for creator in creators:
            self.graph.add((header, DC.creator, Literal(creator)))

        self.graph.add((header, RDFS.comment, Literal("This ontology was generated by Lene https://github.com/mclumd/lene")))

    def add_defaults(self):
        """
        Helper function to add default classes that are expected, but not
        necessarily part of the tree structure. Override this in subclasses
        to construct your graph before parsing the lisp tree.
        """
        Truth = OWLClass("Truth", OWL.Thing, "Truth", "This class should always have two instances, True and False.").bind(self.graph)
        false = Truth.instantiate('false.0', graph=self.graph)
        true  = Truth.instantiate('true.0', graph=self.graph)
        nil   = Truth.instantiate('nil.0', graph=self.graph)

    def add_thing(self, expression):
        """
        Adds to the class hierarchy of the ontology.

        The expression must be in the form of:

            (define-frame NATURE
              (isa (value (non-volitional-agent)))
              ...)

        Frame definitions will be added as subclasses of OWL.Thing
        Attribute Values definitions will be added as instances
        """
        define = expression[0]
        label  = expression[1].title()
        props  = expression[2]

        # We have chosen to parse only define frames to add classes/instances
        assert define in self.DEFINES

        # The isa relationship must be there for us to extract the hierarcy
        assert props[0].lower() == 'isa'

        # Get the parent label by going into the (isa (value (label))) subtree
        # Then construct the parent in the ontology as a placeholder if not bound
        parent = props[1][1][0].title()
        parent = OWLClass(parent)

        if not parent.isbound(self.graph):
            parent.bind(self.graph)

        # If this is an instance, create the instance, otherwise create
        # the class hierarchy as defined. If already in the graph, update.
        if define == DEFINE_ATTRIBUTE_VALUE:
            # Add instance to the graph through the parent
            thing = parent.instantiate(label, graph=self.graph)
        else:
            thing  = OWLClass(label, parent)
            # Update by remove old/add new -- then add to graph
            if thing.isbound(self.graph): thing.unbind(self.graph)
            thing.bind(self.graph)

        return thing

    def add_relation(self, expression):
        """
        Adds an Object Property based on the domain and co-domain of the
        relation in the Lisp representation. Handles the slot attribute.

        The expression must be in the form of:

            (define-relation TEMPERATURE
                (isa            (value (physical-object-attribute)))
                (domain         (value (physical-object)))
                (co-domain      (value (temperature-value)))
                (slot           (value (temperature)))
                )

        Relation definitions will be added as subclasses of OWL.ObjectProperty
        """
        define = expression[0]
        label  = expression[1].title()
        props  = dict(expression[2:])

        # We have chosen to parse only define frames to add classes/instances
        assert define == DEFINE_RELATION

        # The isa, domain, co-domain, and slot must be present
        for key in ('isa', 'domain', 'co-domain', 'slot'):
            assert key in props

        # Get the parent label by going into the (isa (value (label))) subtree
        # Then construct the parent in the ontology as a placeholder if not bound
        parent = props['isa'][1][0].title()
        parent = OWLObjectProperty(parent)
        if not parent.isbound(self.graph):
            parent.bind(self.graph)

        # Get the domain and co-domain from the properties and construct
        # them in the ontology if their placeholder isn't found.
        domain   = props['domain'][1][0].title()
        domain   = OWLClass(domain)

        codomain = props['co-domain'][1][0].title()
        codomain = OWLClass(codomain)

        # Retreive the slot to use as label
        slot     = props['slot'][1][0]

        # Is there some way to insantiate a relation?
        # Actually, come to think of it, I don't see a lot of instances in the reps

        relation = OWLObjectProperty(label, parent, domain, codomain, slot)

        # Update by remove old/add new -- then add to graph
        if relation.isbound(self.graph): relation.unbind(self.graph)
        relation.bind(self.graph)

        return relation

    def serialize(self, *args, **kwargs):
        self.graph.bind("dc", DC)
        self.graph.bind("owl", OWL)
        self.graph.bind("umd", UMD)
        
        if 'format' not in kwargs: kwargs['format'] = 'pretty-xml'
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

    # Create Properties
    similarlyPopularTo = OWLObjectProperty("similarlyPopularTo", OWL.topObjectProperty, Plant, Plant)
    similarlyPopularTo.bind(graph)

    # Create and bind an instance of a flower
    orchid   = Flower.instantiate("Orchid", graph=graph)
    magnolia = Flower.instantiate("Magnolia", graph=graph)

    # Create a relationship between flowers
    similarlyPopularTo.instantiate(orchid, magnolia, graph=graph)
    similarlyPopularTo.instantiate(magnolia, orchid, graph=graph)

    # Bind the namespaces to the graph
    graph.bind("dc", DC)
    graph.bind("owl", OWL)
    graph.bind("umd", UMD)
    print graph.serialize()
