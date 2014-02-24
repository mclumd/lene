# lene.parser.lexer
# Lexical analysis for Lene module
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 15:51:24 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: lexer.py [] bengfort@cs.umd.edu $

"""
Lexical analysis for Lene module
"""

##########################################################################
## Imports
##########################################################################

from .tokenize import *
from lene.exceptions import *
from lene.utils import number

##########################################################################
## Helper functions
##########################################################################

def alphanumeric(token):
    """
    Alias for Lexer.is_alphanumeric
    """
    return Lexer.is_alphanumeric(token)

def ignorable(token):
    """
    Alias for Lexer.is_ignorable
    """
    return Lexer.is_ignorable(token)

def print_tree(tree, depth=0):
    """
    Pretty prints a Token tree
    """
    indent = "  " * depth
    for item in tree:
        if isinstance(item, Token):
            print "%s%s" % (indent, item.value)
        else:
            print_tree(item, depth+1)

##########################################################################
## Lexer Class
##########################################################################

class Lexer(object):
    """
    Takes as input an iterable of tokens and returns a Python data
    structure capable of representing complex Lisp structures and frames.

    The lexer handles all the semantic properties of the parser, whereas
    the tokenizer simply breaks the input stream into its constiuent parts.
    This class also casts numbers into values, and determines what tokens
    to skip or not to skip.
    """

    ALPHANUMS   = {WORD, XREF, NUMBER, OPERAT}
    IGNORABLE   = {COMMENT,}
    PARENTHESES = {RBRACE, LBRACE}

    @classmethod
    def is_alphanumeric(klass, token):
        """
        Checks if a token is alphanumeric, e.g. a WORD, XREF, NUMBER, or
        OPERAT. Note that any new tokens MUST be checked in this method.
        """
        return token.tag in klass.ALPHANUMS

    @classmethod
    def is_ignorable(klass, token):
        """
        Checks if the token is ignorable, e.g. a COMMENT (whitespace is
        already handled by the Tokenizer).
        """
        return token.tag in klass.IGNORABLE

    def parse(self, tokens):
        """
        Reads through the token stream and returns a python data structure
        Essentially returns a list of lists to evaluate. The parser is
        implemented via a typical Recursive Descent algorithm.

        Tokens should be an iterable, highly recommend it's a TokenStream.
        """

        def recursive_descent(lexer, tokens, depth=0):
            """
            Inner helper function that performs recursive descent parsing.

            TODO: Make this function better...
            TODO: Check for unbalanced parentheses in LBRACE elif
            TODO: Handle StopIteration better
            """

            # Create the list of children
            tree  = []
            while True:
                # Get next token and perform per-token-type handling
                try:
                    token = next(tokens)
                except StopIteration:
                    break

                token = lexer.handle_token(token)

                if lexer.is_alphanumeric(token):
                    tree.append(token)
                elif lexer.is_ignorable(token):
                    continue
                elif token.tag == RBRACE:
                    tree.append(recursive_descent(lexer, tokens, depth+1))
                elif token.tag == LBRACE:
                    return tree
                else:
                    raise SyntacticError("Unknown Token '%s'" % repr(token))

            if depth == 0:
                # We're at root
                return tree
            else:
                raise SyntacticError("Unbalanced parentheses")

        tokens = iter(tokens)
        return recursive_descent(self, tokens)

    def handle_token(self, token):
        """
        Farms out token handling to each tag type. Returns a token.
        """
        method = 'handle_%s_token' % token.tag.lower()
        if hasattr(self, method):
            method = getattr(self, method)
            return method(token)
        return token

    def handle_number_token(self, token):
        """
        Casts a number as either an integer or a float.
        """
        value = number(token.value)
        return Token(token.tag, value, token.line, token.column)

    def detokenize(self, tree):
        """
        Walk the tree and detokenize for use in other applications
        """
        for item in tree:
            if isinstance(item, Token):
                yield item.value
            else:
                yield list(self.detokenize(item))
