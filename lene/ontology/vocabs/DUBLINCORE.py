# lene.vocabs.DUBLINCORE
# Vocabulary for the DUBLINCORE Elements
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  timestamp
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: DUBLINCORE.py [] bengfort@cs.umd.edu $

"""
Vocabulary for the DUBLINCORE Elements

See creator: michelepasin.org
See reference: https://github.com/lambdamusic/ontosPy/blob/master/vocabs/DUBLINCORE.py
"""

##########################################################################
## Imports
##########################################################################

from rdflib import Namespace

##########################################################################
## Namespace
##########################################################################

DCNS = Namespace("http://purl.org/dc/elements/1.1/")

##########################################################################
## DUBLINCORE Vocabulary
##########################################################################

contributor = DCNS["contributor"]
coverage    = DCNS["coverage"]
creator     = DCNS["creator"]
date        = DCNS["date"]
description = DCNS["description"]
format      = DCNS["format"]
identifier  = DCNS["identifier"]
language    = DCNS["language"]
publisher   = DCNS["publisher"]
relation    = DCNS["relation"]
rights      = DCNS["rights"]
source      = DCNS["source"]
subject     = DCNS["subject"]
title       = DCNS["title"]
type        = DCNS["type"]
