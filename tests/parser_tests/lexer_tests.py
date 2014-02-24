# tests.parser_tests.lexer_tests
# Tests for the lexical analysis module for lene
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 15:51:24 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: lexer_tests.py [] bengfort@cs.umd.edu $

"""
Tests for the lexical analysis module for lene
"""

##########################################################################
## Imports
##########################################################################

import unittest

from StringIO import StringIO
from lene.utils import flatten
from lene.parser.lexer import *
from lene.parser.tokenize import *
from lene.exceptions import SyntacticError
from tokenize_tests import fixture, simple_fixture

##########################################################################
## Test Cases
##########################################################################

class LexerTests(unittest.TestCase):
    """
    Tests the lexer module with a token stream
    """

    def setUp(self):
        self.tokens = TokenStream(StringIO(fixture))

    def tearDown(self):
        self.tokens = None

    def test_tag_class(self):
        """
        Ensure that Tag classes in Lexer match TAG list
        """
        tags = Lexer.ALPHANUMS | Lexer.IGNORABLE | Lexer.PARENTHESES
        self.assertEqual(tags, Tags)

    def test_is_alphanumeric(self):
        """
        Ensure expected tags are ALPHANUMS
        """
        tokens = (
            Token(WORD, 'goal-scene', 8, 12),
            Token(XREF, '=actor', 14, 21),
            Token(NUMBER, '3.14', 8, 12),
            Token(OPERAT, '+', 3, 28),
        )

        # Test the class method on Lexer
        for token in tokens:
            self.assertTrue(Lexer.is_alphanumeric(token))

        # Test the module helper function is an alias
        msg = "alphanumeric function is not exact alias of Lexer classmethod"
        for token in tokens:
            self.assertEqual(Lexer.is_alphanumeric(token),
                             alphanumeric(token), msg=msg)

    def test_is_not_alphanumeric(self):
        """
        Ensure expected tags are NOT ALPHANUMS
        """
        tokens = (
            Token(RBRACE, '(', 2, 37),
            Token(LBRACE, ')', 7, 38),
            Token(COMMENT, '; Same actor as above\n', 11, 35),
        )

        # Test the class method on Lexer
        for token in tokens:
            self.assertFalse(Lexer.is_alphanumeric(token))

        # Test the module helper function is an alias
        msg = "alphanumeric function is not exact alias of Lexer classmethod"
        for token in tokens:
            self.assertEqual(Lexer.is_alphanumeric(token),
                             alphanumeric(token), msg=msg)

    def test_is_ignorable(self):
        """
        Ensure expected tags are IGNORABLE
        """
        tokens = (
            Token(COMMENT, '; Same actor as above\n', 11, 35),
        )

        # Test the class method on Lexer
        for token in tokens:
            self.assertTrue(Lexer.is_ignorable(token))

        # Test the module helper function is an alias
        msg = "ignorable function is not an exact alias of Lexer classmethod"
        for token in tokens:
            self.assertEqual(Lexer.is_ignorable(token),
                             ignorable(token), msg=msg)

    def test_is_not_ignorable(self):
        """
        Ensure expected tags are NOT IGNORABLE
        """
        tokens = (
            Token(RBRACE, '(', 2, 37),
            Token(LBRACE, ')', 7, 38),
            Token(WORD, 'goal-scene', 8, 12),
            Token(XREF, '=actor', 14, 21),
            Token(NUMBER, '3.14', 8, 12),
            Token(OPERAT, '+', 3, 28),
        )

        # Test the class method on Lexer
        for token in tokens:
            self.assertFalse(Lexer.is_ignorable(token))

        # Test the module helper function is an alias
        msg = "ignorable function is not an exact alias of Lexer classmethod"
        for token in tokens:
            self.assertEqual(Lexer.is_ignorable(token),
                             ignorable(token), msg=msg)

    def test_handle_token(self):
        """
        Ensure that token handling returns a token!
        """
        tokens = (
            Token(RBRACE, '(', 2, 37),
            Token(LBRACE, ')', 7, 38),
            Token(COMMENT, '; Same actor as above\n', 11, 35),
            Token(WORD, 'goal-scene', 8, 12),
            Token(XREF, '=actor', 14, 21),
            Token(NUMBER, '3.14', 8, 12),
            Token(OPERAT, '+', 3, 28),
        )

        self.assertEqual(set(token.tag for token in tokens), Tags,
            msg="Testing error, not all tags represented.")

        lexer = Lexer()
        for token in tokens:
            self.assertTrue(isinstance(lexer.handle_token(token), Token))

    def test_handle_number_token(self):
        """
        Assert that Lexer converts floats and ints
        """
        lexer = Lexer()
        t1 = Token(NUMBER, '3.14', 8, 12)
        t2 = Token(NUMBER, '42', 8, 12)

        t1 = lexer.handle_number_token(t1)
        self.assertTrue(isinstance(t1.value, float))

        t2 = lexer.handle_number_token(t2)
        self.assertTrue(isinstance(t2.value, int))

    def test_simple_parse(self):
        """
        Test the parsing mechanism
        """
        lexer  = Lexer()
        tokens = TokenStream(StringIO(simple_fixture))
        parse  = lexer.parse(tokens)

        expected = [
            [Token(tag='WORD', value='define-frame', line=2, column=2),
             Token(tag='WORD', value='BURNS', line=2, column=15),
                [Token(tag='WORD', value='isa', line=3, column=4),
                    [Token(tag='WORD', value='value', line=3, column=9),
                        [Token(tag='WORD', value='violent-mop', line=3, column=16)]
                    ]
                ],
                [Token(tag='WORD', value='actor', line=4, column=4),
                    [Token(tag='WORD', value='value', line=5, column=6),
                        [Token(tag='WORD', value='non-volitional-agent', line=5, column=13)]
                        ]
                    ],
                    [Token(tag='WORD', value='object', line=6, column=4),
                        [Token(tag='WORD', value='value', line=7, column=6),
                            [Token(tag='WORD', value='physical-object', line=7, column=13)]
                        ]
                    ]
                ]
            ]

        self.assertEqual(expected, parse)

    def test_flatten_parse(self):
        """
        Assert a parse can be flattened
        """
        lexer  = Lexer()
        tokens = TokenStream(StringIO(simple_fixture))
        parse  = lexer.parse(tokens)
        flat   = list(flatten(parse))

        expected = [
            Token(tag='WORD', value='define-frame', line=2, column=2),
            Token(tag='WORD', value='BURNS', line=2, column=15),
            Token(tag='WORD', value='isa', line=3, column=4),
            Token(tag='WORD', value='value', line=3, column=9),
            Token(tag='WORD', value='violent-mop', line=3, column=16),
            Token(tag='WORD', value='actor', line=4, column=4),
            Token(tag='WORD', value='value', line=5, column=6),
            Token(tag='WORD', value='non-volitional-agent', line=5, column=13),
            Token(tag='WORD', value='object', line=6, column=4),
            Token(tag='WORD', value='value', line=7, column=6),
            Token(tag='WORD', value='physical-object', line=7, column=13),
        ]

        self.assertEqual(expected, flat)

    def test_extensive_parse(self):
        """
        Test the parser on a complete fixture
        """

        try:
            lexer = Lexer()
            parse = lexer.parse(self.tokens)
        except SyntacticError:
            self.fail("Was unable to parse the extended fixture.")

    def test_ignore_comments(self):
        """
        Assert that comments are not in parse
        """
        lexer  = Lexer()
        parse  = lexer.parse(self.tokens)
        self.assertNotIn(COMMENT, set(token.tag for token in flatten(parse)))

    def test_unbalanced_parens(self):
        """
        Assert non-balanced parens raises error
        """
        with self.assertRaises(SyntacticError):
            tokens = TokenStream(StringIO("(a (b c (d e (f (g))"))
            lexer  = Lexer()
            lexer.parse(tokens)

    def test_assert_unknown_token(self):
        """
        Assert SyntacticError on unknown token
        """
        tokens = [
            # The following should be correctly evaluated
            Token(tag='WORD', value='define-frame', line=2, column=2),
            Token(tag='WORD', value='BURNS', line=2, column=15),
            Token(tag='WORD', value='isa', line=3, column=4),
            Token(tag='WORD', value='value', line=3, column=9),
            Token(tag='WORD', value='violent-mop', line=3, column=16),

            # Error should be raised on the following tag
            Token(tag='ACTOR', value='actor', line=4, column=4),

            # Following should not be evaluated
            Token(tag='WORD', value='value', line=5, column=6),
            Token(tag='WORD', value='non-volitional-agent', line=5, column=13),
            Token(tag='WORD', value='object', line=6, column=4),
            Token(tag='WORD', value='value', line=7, column=6),
            Token(tag='WORD', value='physical-object', line=7, column=13),
        ]

        with self.assertRaises(SyntacticError):
            lexer  = Lexer()
            lexer.parse(tokens)

    def test_detokenize(self):
        """
        Test the detokenize method to extract values
        """
        lexer  = Lexer()
        tokens = TokenStream(StringIO(simple_fixture))
        parse  = lexer.parse(tokens)
        tree   = list(lexer.detokenize(parse))
        expect = [
            ['define-frame',
             'BURNS',
                ['isa',
                    ['value',
                        ['violent-mop']
                    ]
                ],
                ['actor',
                    ['value',
                        ['non-volitional-agent']
                    ]
                ],
                ['object',
                    ['value',
                        ['physical-object']
                    ]
                ]
            ]
        ]

        self.assertEqual(tree, expect)
