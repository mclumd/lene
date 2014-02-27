# lene.parser.tokenize
# Simple tokenizer for Lisp representations
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 09:38:10 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: tokenize.py [] bengfort@cs.umd.edu $

"""
Simple tokenizer for Lisp representations.

This class contains a Tokenizer that accepts a string, tokenizing it into
a suitable grammar as it goes. This tokenizer makes heavy use of Regular
Expressions for the Grammar, is is particularly concerned with the
parenthetical representations of frames in META-Aqua.

The tokenizer is based on the Regex tokenizer from:
    http://docs.python.org/3.2/library/re.html#writing-a-tokenizer

TODO: Comments must have newlines (fix)
TODO: ':' symbol for package imports raises exception
"""

##########################################################################
## Imports
##########################################################################

import re
import collections

from lene.exceptions import *

##########################################################################
## Tag and Module Constants
##########################################################################

Token   = collections.namedtuple('Token', ['tag', 'value', 'line', 'column'])

RBRACE  = 'RBRACE'
LBRACE  = 'LBRACE'
NEWLINE = 'NEWLINE'
SKIP    = 'SKIP'
COMMENT = 'COMMENT'
WORD    = 'WORD'
XREF    = 'XREF'
NUMBER  = 'NUMBER'
OPERAT  = 'OPERAT'

Tags    = {RBRACE, LBRACE, COMMENT, WORD, XREF, NUMBER, OPERAT,}

##########################################################################
## Tokenization
##########################################################################

class Tokenizer(object):

    SPECIFICATION = {
        RBRACE:  r'\(',                       # Opening brace
        LBRACE:  r'\)',                       # Closing brace
        NEWLINE: r'\n',                       # Line endings
        SKIP:    r'[ \t]',                    # Skip over spaces and tabs
        COMMENT: r';.*\n',                    # Capture comments
        WORD:    r'[a-zA-Z_][\w\._\-><\?]*',  # Identifiers as words
        XREF:    r'[=:][a-zA-Z_][\w\._-]*',   # Cross reference to other values
        NUMBER:  r'[-+]?[\d]*\.?[\d]+',       # Signed integers or floating point
        OPERAT:  r'[+*\/\-%]',                # Arithmetic operators
    }

    KEYWORDS      = set([])

    def __init__(self, specification=None, keywords=None):
        """
        User can add additional (or override) specifications and keywords
        at runtime by passing them into the instantiation of this class.
        """

        # Create defaults then update specification
        self.specification = self.SPECIFICATION.copy()
        if specification:
            self.specification.update(specification)

        # Create defaults then update keywords
        self.keywords      = self.KEYWORDS.copy()
        if keywords:
            self.keywords.update(keywords)

    @property
    def token_regex(self):
        """
        Property that automatically compiles token specification into a
        regular expression, and stores that compilation for further use.
        """
        if not hasattr(self, '_compiled_token_regex'):
            regex_str = "|".join('(?P<%s>%s)' % item for item in self.specification.items())
            self._compiled_token_regex = re.compile(regex_str)
        return self._compiled_token_regex

    def get_token(self, *args, **kwargs):
        """
        Alias for re.compile(token_regex).match
        """
        return self.token_regex.match(*args, **kwargs)

    def tokenize(self, stream):
        """
        Breaks a stream into its constiuent tokens via the tokenizer regex
        """

        # Initialize internal function vars
        line = 1
        pos = lns = 0
        mob = self.get_token(stream)

        while mob is not None:
            tag = mob.lastgroup

            if tag == NEWLINE:
                lns = pos   # Keep track of string continuation
                line += 1   # Increment the line number

            elif tag != SKIP:
                val = mob.group(tag)

                # Tags according to Keyword, is this a good idea?
                if tag == WORD and val in self.keywords:
                    tag = val

                yield Token(tag, val, line, mob.start()-lns)

            pos = mob.end()
            mob = self.get_token(stream, pos)

        if pos != len(stream):
            raise UnexpectedCharacter(stream[pos], line)

##########################################################################
## Token Stream
##########################################################################

class TokenStream(object):
    """
    Expects a file-like object with a `read` method, otherwise treats the
    fp as a path and attempts to open it. It then uses the tokenizer class
    to read the file from disk and generate tokens.
    """

    tokenizer_class = Tokenizer

    def __init__(self, fp, tokenizer=None):
        """
        Pass in fp, an file-like object, or a path to open. You can also
        pass in a custom Tokenizer class if desired, otherwise it will use
        the default `tokenizer_class` on the class
        """
        if not hasattr(fp, 'read'):
            fp = open(fp, 'r')

        self.stream    = fp
        self.tokenizer = tokenizer or self.tokenizer_class()

    def __iter__(self):
        """
        Reads in entire stream, closes the fp and then yields each token.
        """
        self._stream = self.stream.read()
        self.stream.close()

        for token in self.tokenizer.tokenize(self._stream):
            yield token
