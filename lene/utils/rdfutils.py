# lene.utils.rdfutils
# Utility functions for managing rdf and OWL
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Mar 25 14:14:34 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: rdfutils.py [] bengfort@cs.umd.edu $

"""
Utility functions for managing rdf and OWL
"""

##########################################################################
## Imports
##########################################################################

from os.path import splitext
from urlparse import urlparse
from rdflib import URIRef, RDFS, RDF, BNode

##########################################################################
## Utility functions
##########################################################################

def sort_by_namespace_prefix(uris, namespaces):
    """
    Given an ordered list of namespace prefixes, order a list of uris.

    E.g.
        uris = [
            rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
            rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')
        ]

        uris = sort_by_namespace_prefix(uris, [OWL.OWLNS, RDFS])
        uris => [
            rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
            rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        ]

    TODO: This can be better, remove multiple iterations over uris list.
    """
    output = []
    uris   = sort_uri_list_by_name(uris)
    for ns in namespaces:
        output.extend(list(filter_by_namespace_prefix(uris, ns)))

    # Add any remaining uris
    for uri in uris:
        if uri not in output:
            output.append(uri)

    return output

def filter_by_namespace_prefix(uris, namespace):
    """
    Filter a list of uris by their namespace
    """
    for uri in uris:
        if str(uri).startswith(str(namespace)):
            yield uri

def sort_uri_list_by_name(uris):
    """
    Sorts a list of uris based on the last bit (usually the name) of a uri
    It checks whether the last bit is specified using a # or just a /, eg:
            rdflib.URIRef('http://purl.org/ontology/mo/Vinyl'),
            rdflib.URIRef('http://purl.org/vocab/frbr/core#Work')

    """

    def get_last_bit(uri_string):
        try:
            x = uri_string.split("#")[1]
        except:
            x = uri_string.split("/")[-1]
        return x

    try:
        return sorted(uris, key=lambda x: get_last_bit(x.__str__()))
    except:
        # TODO: do more testing.. maybe use a unicode-safe method instead of __str__
        print "Error in <sort_uri_list_by_name>: possibly a UnicodeEncodeError"
        return uris

def is_blank(node):
    """
    Determines if a Class is a blank node.
    """
    return type(node) == BNode

def infer_namespace_prefix(uri):
    """
    From a URI returns the last bit and simulates a namespace prefix.
    e.g. <'http://www.w3.org/2008/05/skos#'> returns the 'skos' string
    """
    uristr = str(uri)
    parts  = uristr.replace("#", "").split("/")
    if parts: return parts[-1]
    return ""

def guess_rdf_format(uri):
    """
    Simple file format guessing, using rdflib format types based on the
    file extension or suffix. See rdflib.parse for more information:
        [https://rdflib.readthedocs.org/en/latest/using_graphs.html]
    """

    XML  = "xml"
    NT   = "nt"
    N3   = "n3"
    TRIX = "trix"
    RDFA = "rdfa"

    extmap = {
        ".xml":  XML,
        ".nt":   NT,
        ".n3":   N3,
        ".ttl":  N3,
        ".trix": TRIX,
        ".rdfa": RDFA,
        ".owl":  XML,
        ".rdf":  XML,
    }

    # Split extension from URI
    path = urlparse(uri).path
    ext  = splitext(path)[1].lower()

    # Return via mapping
    if ext in extmap:
        return extmap[ext]
    return XML
