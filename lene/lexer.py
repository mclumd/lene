# lene.lex
# Simple lexical analysis for Lisp representations
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  timestamp
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: lex.py [] bengfort@cs.umd.edu $

"""
Simple lexical analysis for Lisp representations.

This class contains a Lexer that accepts a Stream and reads that stream,
tokenizing it into a suitable grammar as it goes. This lexer makes heavy
use of Regular Expressions for the Grammar, is is particularly concerned
with the parenthetical representations of frames in META-Aqua.

The tokenizer of the stream to pass to the lexical analysis is from:
    http://docs.python.org/3.2/library/re.html#writing-a-tokenizer
"""

##########################################################################
## Imports
##########################################################################

import re
import collections

from .exceptions import *

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

Tags    = {RBRACE, LBRACE, COMMENT, WORD, XREF}

##########################################################################
## Tokenization
##########################################################################

class Tokenizer(object):

    SPECIFICATION = {
        RBRACE:  r'\(',           # Opening brace
        LBRACE:  r'\)',           # Closing brace
        NEWLINE: r'\n',           # Line endings
        SKIP:    r'[ \t]',        # Skip over spaces and tabs
        COMMENT: r';.*\n',         # Capture comments
        WORD:    r'[\d\w\._-]+',  # Identifiers as words
        XREF:    r'=',            # Cross reference to other values
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

if __name__ == '__main__':

    tokenizer = Tokenizer()
    for token in tokenizer.tokenize(stmts): print token
