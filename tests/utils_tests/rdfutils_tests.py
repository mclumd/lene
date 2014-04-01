# tests.utils_tests.rdfutils_tests
# Testing for the rdfutils package in Lene
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Mar 25 17:31:13 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: rdfutils_tests.py [] bengfort@cs.umd.edu $

"""
Testing for the rdfutils package in Lene
"""

##########################################################################
## Imports
##########################################################################

import unittest
import rdflib.term

from lene.utils.rdfutils import *
from lene.vocabs import OWL
from rdflib import RDFS, BNode

##########################################################################
## TestCases
##########################################################################

class RDFUtilsTests(unittest.TestCase):

    def test_namespace_sort(self):
        """
        Test the RDF sort by namespace utility
        """
        uris = [
            rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
            rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')
        ]

        uris = sort_by_namespace_prefix(uris, [OWL.OWLNS, RDFS])
        self.assertEqual(uris, [
            rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
            rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        ])

    def test_namespace_filter(self):
        """
        Test the RDF filter by namespace utility
        """
        uris = [
            rdflib.term.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#comment'),
            rdflib.term.URIRef(u'http://www.w3.org/2000/01/rdf-schema#label'),
            rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass')
        ]

        uris = list(filter_by_namespace_prefix(uris, OWL.OWLNS))
        self.assertEqual(uris, [
            rdflib.term.URIRef(u'http://www.w3.org/2002/07/owl#equivalentClass'),
        ])

    @unittest.skip
    def test_uri_name_sort(self):
        """
        Test the URI name sort utility
        """
        # TODO: Implement
        pass

    def test_is_blank(self):
        """
        Test the blank node checker
        """
        self.assertTrue(is_blank(BNode()))
        self.assertFalse(is_blank("bob"))

    def test_rdf_format_guesser(self):
        """
        Test the rdf format guessing
        """

        tests = (
            ("http://bigasterisk.com/foaf.rdf", "xml"),
            ("/home/ubuntu/mclumd.owl", "xml"),
            ("/home/ubuntu/mclumd.ttl", "n3"),
            ("http://cs.umd.edu/active/ontology.rdfa", "rdfa"),
            ("http://cs.umd.edu/active/ontology.json", "xml"),
        )

        for uri, fmt in tests:
            self.assertEqual(fmt, guess_rdf_format(uri))
