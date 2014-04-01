# lene.ontology
# Creates an RDF/OWL ontology from a KB
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Mar 25 12:16:39 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: ontology.py [] bengfort@cs.umd.edu $

"""
Creates an RDF/OWL ontology from a KB
"""

##########################################################################
## Imports
##########################################################################

import rdflib
import urllib2
import operator

from utils.rdfutils import *
from vocabs import OWL, DUBLINCORE as DC
from rdflib import Namespace, exceptions, URIRef, RDFS, RDF, BNode

##########################################################################
## Module Constants
##########################################################################

DEFAULT_SESSION_NAMESPACE = "http://www.example.org/session/resource#"
DEFAULT_ONTO = "http://xmlns.com/foaf/0.1/"
DEFAULT_LANGUAGE = "en"

##########################################################################
## The Ontology
##########################################################################

class Ontology(object):
    """
    A class that includes methods for manipulating an RDF/RDFS/OWL graph
    at the ontological level.
    """

    def __init__(self, uri=None):
        """
        Class that includes methods for manipulating an RDF/RDFS/OWL graph
        at the ontological level. If no URI is specified, then an empty
        ontology is constructed.

        :param uri: a valid ontology uri (could be a local file path too)
        """
        self.graph      = rdflib.Graph()
        self.pretty_uri = None
        self.location   = None

        self.classes    = None
        self.instances  = None
        self.rdf_props  = None
        self.obj_props  = None
        self.data_props = None
        self.inferred   = None
        self.properties = None

        self.toplayer   = None
        self.max_depth  = None
        self.session    = None
        self.session_ns = None

        self.class_tree = None

        # If a URI is passed in, then load it from the location.
        self.load(uri)

    def load(self, uri):
        """
        Loads a URI using the rdflib parser, which can include a web URI.
        What happens with multiple load calls? Should this be a class
        method that returns an instance of the ontology?
        """

        if not uri: return                      # Handle empty URIs
        if uri.startswith("www."):              # Handle lazy URLs
            uri = "http://%s" % str(uri)

        # Guess the format and parse
        rdffmt = guess_rdf_format(uri)
        self.graph.parse(uri, format=rdffmt)    # Handle exceptions?

        # Instantiate properties from the loaded graph
        self.location   = uri
        self.pretty_uri = self.get_ontology_uri(stringify=True, exclude_blank=True)

    def dump(self, path):
        """
        Save the current ontology to the path on disk.
        """
        with open(path, 'wb') as out:
            out.write(self.serialize())

    def __repr__(self):
        return "<%s for URI: %s - %d triples>" % (
            self.__class__.__name__, self.pretty_uri, len(self.graph))

    ##////////////////////////////////////////////////////////////////////
    ## Methods for handling RDF resources (entities)
    ##////////////////////////////////////////////////////////////////////

    def entity_triples(self, entity, prettify=False, exclude_props=None,
            exclude_blank=False, order_props=[RDF, RDFS, OWL.OWLNS, DC.DCNS]):
        """
        Returns the pred-obj for any given resource, excluding selected.

        Sorting: by default results are sorted alphabeticallya nd according
        to the namespaces listed in the order_props default list.
        """
        output  = []
        exclude = exclude_props if exclude_props is not None else []
        for s,p,o in self.graph.triples((entity, None, None)):
            if exclude_blank and is_blank(o): continue
            if p not in exclude:
                output.append((p,o))

        # Sorting
        if type(order_props) == type([]):
            ordered = sort_by_namespace_prefix([p for p,o in output], order_props)
            ordered = [(n+1, x) for n,x in enumerate(ordered)]
            ranked  = dict((key, rank) for (rank, key) in ordered)
            output  = sorted(output, key=lambda tup: ranked.get(tup[0]))
        elif order_props:
            output  = sorted(output, key=operator.itemgetter(0))

        if prettify:
            return [(self.uri2nice(p), o) for p,o in output]
        return output

    def entity_labels(self, entity, language=DEFAULT_LANGUAGE, getall=True):
        """
        Returns the rdfs.label value of an entity (class or property), if
        it exists; the default is the DEFAULT_LANGUAGE. Returns the
        RDF.Literal resource.
        """

        if getall:
            return list(self.graph.objects(entity, RDFS.label))

        for obj in self.graph.objects(entity, RDFS.label):
            if hasattr(obj, 'language') and getattr(obj, 'language') == language:
                return obj
        return ""

    def entity_comment(self, entity, language=DEFAULT_LANGUAGE, getall=True):
        """
        Returns the rdfs.comment value of an entity (class or property) if
        it exists; the default is the DEFAULT_LANGUAGE. Returns the
        RDF.Literal resource.
        """
        if getall:
            return list(self.graph.objects(entity, RDFS.comment))

        for obj in self.graph.objects(entity, RDFS.comment):
            if hasattr(obj, 'language') and getattr(obj, 'language') == language:
                return obj
        return ""

    ##////////////////////////////////////////////////////////////////////
    ## Methods for handling ontologies
    ##////////////////////////////////////////////////////////////////////

    def get_ontology_uri(self, stringify=False, exclude_blank=False, try_dcmeta=False):
        """
        Returns the ontology URI if defined using the pattern:
            <uri> a http://www.w3.org/2002/07/owl#Ontology

        In other cases it returns None (and Ontology defaults to the URI
        passed at loading time). Blank nodes can be excluded for pretty
        printing if needed. If a blank node is found, you can also try to
        search the DC metadata.
        """

        nodes = [x for x in self.graph.subjects(RDF.type, OWL.Ontology)]

        # Couldn't find any ontology subjects
        if not nodes:
            return None

        # Check if the search result is blank
        if is_blank(nodes[0]):

            if exclude_blank:
                return None

            if try_dcmeta:
                dcids = [x for x in self.graph.objects(nodes[0]), DC.identifier]
                if dcids:
                    return str(dcids[0]) if stringify else dcids[0]

        # Return the result, stringified as needed
        return str(nodes[0]) if stringify else nodes[0]

    def annotations(self, prettify=False, exclude_props=False, exclude_blank=False):
        """
        Method that tries to get all the available annotations for an OWL
        ontology. Returns a list of (uri, values) where values is a list.
        """
        return self.entity_triples(self.get_ontology_uri(), prettify=prettify,
                     exclude_props=exclude_props, exclude_blank=exclude_blank)

    def namespaces(self, base_only=False):
        """
        Exctract the ontology namespaces. If base_only, return the base or
        all of the namespaces. Namespaces are given in the format:

            for x in rdfGraph.namespaces(): print x

            ('xml', rdflib.URIRef('http://www.w3.org/XML/1998/namespace'))
            ('', rdflib.URIRef('http://cohereweb.net/ontology/cohere.owl#'))
            (u'owl', rdflib.URIRef('http://www.w3.org/2002/07/owl#'))
            ('rdfs', rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#'))
            ('rdf', rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'))
            (u'xsd', rdflib.URIRef('http://www.w3.org/2001/XMLSchema#'))
        """

        if base_only:
            ll = [x for x in self.graph.namespaces() if x[0] == '']
            if ll: return ll[0][1]
            return None
        else:
            output = []
            for x in self.graph.namespaces():
                if x[0]: output.append(x)
            else:
                prefix = infer_namespace_prefix(x[1])
                if not prefix:
                    prefix = "base"
                output.append((prefix, x[1]))

            return sorted(output)

    def statistics(self):
        """
        Returns a list of tuples containing interesting stats.
        """
        return [
            ("Triples", len(self.graph)),
            ("Classes", len(self.classes)),
            ("Object Properties", len(self.obj_props)),
            ("Datatype Properties", len(self.data_props)),
            ("Individuals", len(self.instances)),
        ]

    def serialize(self, format=""):
        """
        Shortcut to output the ontology graph.
        """
        if format: return self.graph.serialize(format=format)
        return self.graph.serialize()

    ##////////////////////////////////////////////////////////////////////
    ## Methods for manipulating OWL classes
    ##////////////////////////////////////////////////////////////////////

    def _get_all_classes(self, predicate="", **kwargs):
        """
        Extracts all classes from an RDF graph using RDFS and OWL predicate
        by default and extracting non explicitly declared classes. Keep in
        mind that OWL:Thing is by defawult the class of all OWL classes.

        Arguments:
            predicate: 'rdfs' or 'owl' (defaults to "" == both)
            include_domain_range: boolean (False)
            include_implicit: boolean (False)
            remove_blank: boolean (True)
            add_owl_thing: boolean (True)
            exclude_rdf_owl: boolean (True)
        """

        def add_to_dict(key, data):
            if kwargs.get('exclude_rdf_owl', True):
                nspaces = (
                    'http://www.w3.org/2002/07/owl#',
                    'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                    'http://www.w3.org/2000/01/rdf-schema#',
                )
                for ns in nspaces:
                    if key.startswith(ns): return data

            data.add(key)
            return data

        output = set([])

        if kwargs.get('add_owl_thing', True):
            output = add_to_dict(OWL.Thing, output)

        if predicate in ("", "rdfs"):
            for subj in self.graph.subjects(RDF.type, RDFS.Class):
                output = add_to_dict(subj, output)

        if predicate in ("", "owl"):
            for subj in self.graph.subjects(RDF.type, OWL.Class):
                output = add_to_dict(subj, output)

        if kwargs.get("include_domain_range", False):
            for obj in self.graph.objects(None, RDFS.domain):
                output = add_to_dict(obj, output)
            for obj in self.graph.objects(None, RDFS.range):
                output = add_to_dict(obj, output)

        if kwargs.get("include_implicit", False):
            for subj, verb, obj in self.graph.triples((None, RDFS.subClassOf, None)):
                output = add_to_dict(subj, output)
                output = add_to_dict(obj, output)
            for obj in self.graph.objects(None, RDF.type):
                output = add_to_dict(obj, output)

        output = list(output)
        if kwargs.get("remove_blank", True):
            output = [key for key in output if not is_blank(key)]
        return sort_uri_list_by_name(output)

    def _get_top_classes(self, predicate='', ignore_thing=True):
        """
        Finds the topclass in the ontology (with multiple inheritance).
        """
        pass

    def _build_class_tree(self, parent=None, out=None):
        """
        Reconstruct the taxonomical tree of an ontology.
        """
        pass

    def _classes_from_tree(self, element=0, out=None):
        """
        Extract all the classes in order from the tree representation of
        the ontology. Useful for taxonomic introspection.
        """
        pass

    def _class_tree_level(self, cls, level=0, key=0):
        """
        Returns the depth of a class in the class tree by inspecting the
        Tree dictionary.
        """
        pass

    def _ontology_max_depth(self):
        """
        Returns the max depth of the ontology class tree.
        """
        pass

    def class_repr(self, cls):
        """
        Returns a dictionary with chosen attributes of the class.
        """
        pass

    def class_find(self, name, exact=False):
        """
        Finds a class from its name within an ontology graph.
        """
        pass

    def class_superclasses(self, cls, direct=True, exclude_blank=True, sort=False):
        """
        Returns a list of the super classes for a particular class. If
        direct is True, then it only returns the direct superclasses,
        otherwise it returns all of the superclasses.
        """
        pass

    def class_subclasses(self, cls, direct=True, exclude_blank=True, sort=False):
        """
        Returns a list of the subclasses for a particular class. If direct
        is True, then it returns the direct children, otherwise it returns
        all ancesestors of the given class.
        """
        pass

    def class_siblings(self, cls, exclude_blank=True, sort=False):
        """
        Returns a list of siblings for a given class (direct children of
        the same parent(s)).
        """
        pass

    def class_most_specialized(self, classes):
        """
        From a list of classes, returns the leaf nodes only.
        """
        pass

    def class_most_generic(self, classes):
        """
        From a list of classes, returns only the most generic.
        """
        pass

    def class_domain_for(self, cls, inherited=False):
        """
        Gets all the poperties that declare this class as a domain.
        """
        pass

    def class_range_for(self, cls, inherited=False):
        """
        Gets all the properties that declare this class as a range.
        """
        pass

    def class_properties(self, cls):
        """
        Gets all the properties defined for a class and their values.
        """
        pass

    def class_instances(self, clss, direct=True):
        """
        Gets all the instances of a class (direct instances by default).
        """
        pass

    ##////////////////////////////////////////////////////////////////////
    ## Methods for manipulating OWL properties
    ##////////////////////////////////////////////////////////////////////

    def _get_all_properties(self, predicate="", include_implicit=False):
        """
        Extracts all the properties declared in a model.
        """

        if predicate not in ("", "rdf.property", "owl.objectproperty", "owl.datatypeproperty"):
            raise Exception("Unknown class predicate '%s'" % predicate)

        output = set([])

        if predicate in ("", "rdf.property"):
            for subj in self.graph.subjects(RDF.type, RDF.Property):
                output.add(subj)

            if include_implicit:
                for subj in self.graph.subjects(None, None):
                    output.add(subj)

        if predicate in ("", "owl.objectproperty") or include_implicit:
            for subj in self.graph.subjects(RDF.type, OWL.ObjectProperty):
                output.add(subj)

        if predicate in ("", "owl.datatypeproperty") or include_implicit:
            for subj in self.graph.subjects(RDF.type, OWL.DatatypeProperty):
                output.add(subj)

        output = list(output)
        return sort_uri_list_by_name(output)

    def _get_top_properties(self, predicate='', include_implicit=False):
        """
        Finds the top property in an ontology
        """
        pass

    def _build_property_tree(self, predicate, parent=None, out=None):
        """
        Constructs a taxonomical property tree of an ontology.
        """
        pass

    def property_repr(self, prop):
        """
        Returns a representation of a property
        """
        pass

    def property_find(self, name, exact=False, predicate=", include_implicit"=False):
        """
        Find a property from its name within an ontology graph.
        """
        pass

    def property_range(self, prop):
        """
        Returns the range of a property
        """
        pass

    def property_domain(self, prop):
        """
        Returns the domain of a property
        """
        pass

    def property_superclasses(self, prop, direct=True, exclude_blank=True, sort=False):
        """
        Return a list of superclasses of a property. If direct is True then
        only return immediate superclasses, otherwise return all.
        """
        pass

    def property_subclasses(self, prop, direct=True, exclude_blank=True, sort=False):
        """
        Return a list of subclasses of a property. If direct is True then
        return only immediate subclasses, otherwise return all of them.
        """
        pass

    ##////////////////////////////////////////////////////////////////////
    ## Methods for manipulating OWL instances
    ##////////////////////////////////////////////////////////////////////

    def _get_all_instances(self):
        """
        Returns all of the instances in the ontology
        """
        pass

    def instance_representation(self, instance):
        """
        Similar to the class/property representation for an instance.
        """
        pass

    def instance_find(self, name, exact=False):
        """
        Find an instance by a name.
        """
        pass

    def add_instance(self, cls, instance, ns=None):
        """
        Adds or creates a class-instance to the session-graph and returns
        the instance...
        """
        pass

    def instance_parent(self, instance, most_specialized=True):
        """
        Returns the class of the instance
        """
        pass

    def instance_siblings(self, instance):
        """
        Returns the siblings of an instance.
        """
        pass

    ##////////////////////////////////////////////////////////////////////
    ## Helper methods and utilities
    ##////////////////////////////////////////////////////////////////////

    def uri2nice(self, uri):
        """
        REturns a nice string representation of the uri that also uses the
        namespace symbols. Cuts the uri of the namespace and replaces it
        with its shortcut.
        """
        nice = str(uri)
        for nstup in self.namespaces():
                if nice.find(str(nstup[1])) == 0:
                    if nstup[0]:
                        prefix = nstup[0]
                    else:
                        prefix = infer_namespace_prefix(nstup[1])
                        if not prefix:
                            prefix = "base"

        return prefix + ":" + nice[len(str(nstup[1])):]

    def nice2uri(self, s):
        """
        Returns a URI instance from a string representation.
        """
        pass

    def to_html(self, element=0, treedict=None):
        """
        Builds an HTML tree representation based on the internal tree.
        """
        pass

    def pprint(self, treetype, element=0, treedict=None, level=0):
        """
        Pretty prints either a class tree, an object property tree or the
        datatype property tree depending on the treetype parameter.
        """
        pass

if __name__ == '__main__':
    ontology = Ontology("/Users/benjamin/Repos/umd/lene/fixtures/mclumd.owl")
    entity   = URIRef("http://cs.umd.edu/active/#Action")
    #print ontology.get_ontology_uri()
    #print ontology.namespaces()
    print "\n".join(ontology._get_all_classes())
