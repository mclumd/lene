# encoding: utf-8
# lene.vocabs.OWL
# Vocabulary for the OWL namespace within RDF
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Mar 25 14:07:18 2014 -0400
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: OWL.py [] bengfort@cs.umd.edu $

"""
Vocabulary for the OWL namespace within RDF

See creator: michelepasin.org
See reference: https://github.com/lambdamusic/ontosPy/blob/master/vocabs/OWL.py
"""

##########################################################################
## Imports
##########################################################################

from rdflib import Namespace

##########################################################################
## Namespace
##########################################################################

OWLNS = Namespace("http://www.w3.org/2002/07/owl#")

##########################################################################
## OWL Vocabulary
##########################################################################

AllDifferent        =  OWLNS["AllDifferent"]
allValuesFrom       = OWLNS["allValuesFrom"]
AnnotationProperty  = OWLNS["AnnotationProperty"]
cardinality         = OWLNS["cardinality"]
Class               = OWLNS["Class"]
complementOf        = OWLNS["complementOf"]
DataRange           = OWLNS["DataRange"]
DatatypeProperty    = OWLNS["DatatypeProperty"]
DeprecatedClass     = OWLNS["DeprecatedClass"]
DeprecatedProperty  = OWLNS["DeprecatedProperty"]
differentFrom       = OWLNS["differentFrom"]
disjointWith        = OWLNS["disjointWith"]
distinctMembers     = OWLNS["distinctMembers"]
equivalentClass     = OWLNS["equivalentClass"]
equivalentProperty  = OWLNS["equivalentProperty"]
FunctionalProperty  = OWLNS["FunctionalProperty"]
hasValue            = OWLNS["hasValue"]
imports             = OWLNS["imports"]
incompatibleWith    = OWLNS["incompatibleWith"]
intersectionOf      = OWLNS["intersectionOf"]
InverseFunctionalProperty = OWLNS["InverseFunctionalProperty"]
inverseOf           = OWLNS["inverseOf"]
maxCardinality      = OWLNS["maxCardinality"]
minCardinality      = OWLNS["minCardinality"]
Nothing             = OWLNS["Nothing"]
ObjectProperty      = OWLNS["ObjectProperty"]
oneOf               = OWLNS["oneOf"]
onProperty          = OWLNS["onProperty"]
Ontology            = OWLNS["Ontology"]
OntologyProperty    = OWLNS["OntologyProperty"]
priorVersion        = OWLNS["priorVersion"]
Restriction         = OWLNS["Restriction"]
sameAs              = OWLNS["sameAs"]
someValuesFrom      = OWLNS["someValuesFrom"]
Thing               = OWLNS["Thing"]
TransitiveProperty  = OWLNS["TransitiveProperty"]
unionOf             = OWLNS["unionOf"]
versionInfo         = OWLNS["versionInfo"]
