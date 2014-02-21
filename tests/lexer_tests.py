# tests.lexer_tests
# Testing the lexical analysis and tokenization module
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 10:15:07 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: lexer_tests.py [] bengfort@cs.umd.edu $

"""
Testing the lexical analysis and tokenization module
"""

##########################################################################
## Imports
##########################################################################

import unittest

from lene.lexer import *
from collections import defaultdict

##########################################################################
## Token Object Test Case
##########################################################################

class TokenTests(unittest.TestCase):
    """
    Ensure that the Token class is a namedtuple (or like it) and it works
    as expected to ensure other tests in this library also succeed.
    """

    def test_token_obj(self):
        """
        Ensure tokens have expected attributes
        """
        tok = Token('WORD', 'Metacognitive', 2, 4)
        self.assertEqual(tok.tag, 'WORD')
        self.assertEqual(tok.value, 'Metacognitive')
        self.assertEqual(tok.line, 2)
        self.assertEqual(tok.column, 4)

    def test_token_immutability(self):
        """
        Assert that token is immutable
        """
        tok = Token('WORD', 'Metacognitive', 2, 4)
        with self.assertRaises(AttributeError):
            tok.value = 'Mcl'

##########################################################################
## Tokenizer Test Case
##########################################################################

class TokenizerTest(unittest.TestCase):

    def test_default_specification(self):
        """
        Ensure a default specification
        """
        tokenizer = Tokenizer()
        self.assertTrue(hasattr(tokenizer, 'specification'))
        self.assertIn('NEWLINE', tokenizer.specification)

    def test_default_keywwords(self):
        """
        Ensure default keywords
        """
        tokenizer = Tokenizer()
        self.assertTrue(hasattr(tokenizer, 'keywords'))

    def test_specification_update(self):
        """
        Assert specification is updated at runtime
        """
        tokenizer = Tokenizer(specification={"ASSIGN": r':='})
        self.assertTrue(hasattr(tokenizer, 'specification'))
        self.assertIn('NEWLINE', tokenizer.specification)
        self.assertIn('ASSIGN', tokenizer.specification)

    def test_keywords_update(self):
        """
        Assert keywords are updated at runtime
        """
        tokenizer = Tokenizer(keywords={'IF', 'ELSE', 'THEN'})
        self.assertTrue(hasattr(tokenizer, 'keywords'))
        self.assertIn('IF', tokenizer.keywords)

    def test_token_regex_property(self):
        """
        Test the token_regex property
        """
        tokenizer = Tokenizer(specification={"ASSIGN": r':='})
        self.assertTrue(hasattr(tokenizer, 'token_regex'))
        self.assertTrue(hasattr(tokenizer.token_regex, 'match'))
        self.assertTrue(tokenizer.token_regex.match(':='))

    def test_get_token(self):
        """
        Test the get_token method
        """
        tokenizer = Tokenizer(specification={"ASSIGN": r':='})
        token = tokenizer.get_token(':= bob')
        self.assertTrue(token) # Expecting an SRE_Match object

    def test_simple_tokenize(self):
        """
        Test a simple assignment tokenization
        """
        tokenizer = Tokenizer(specification={"ASSIGN": r':='})
        tokens = list(tokenizer.tokenize("name := bob"))

        # Ensure there are three tokens
        self.assertEqual(len(tokens), 3)

        # Test the first token
        name = tokens[0]
        self.assertEqual(name.tag, 'WORD')
        self.assertEqual(name.value, 'name')
        self.assertEqual(name.line, 1)
        self.assertEqual(name.column, 0)

        # Test the second token
        equals = tokens[1]
        self.assertEqual(equals.tag, 'ASSIGN')
        self.assertEqual(equals.value, ':=')
        self.assertEqual(equals.line, 1)
        self.assertEqual(equals.column, 5)

        # Test the third token
        name = tokens[2]
        self.assertEqual(name.tag, 'WORD')
        self.assertEqual(name.value, 'bob')
        self.assertEqual(name.line, 1)
        self.assertEqual(name.column, 8)

    def test_complex_tokenize(self):
        """
        Test a real example from a representation
        """

        stmts = """
        ;;; The BURNS frame
        (define-frame BURNS
                  (isa (value (violent-mop)))
          (actor
            (value (non-volitional-agent)))
          (object
            (value (physical-object)))
          (goal-scene
            (value (ingest
                 (actor
                   (value =actor)); Same actor as above
                 (object
                   (value =object)) ; Same object as above
                 )))
          (scenes
            (value (=goal-scene))); The scene is the goal scene
          (main-result
            (value (burning
                 (domain (value =object))
                 )))
          )"""

        tokenizer = Tokenizer()
        tokens = list(tokenizer.tokenize(stmts))
        self.assertEqual(len(tokens), 87)

        # Count the various tags
        tag_count = defaultdict(int)
        for token in tokens:
            tag_count[token.tag] += 1

        # Ensure that all tags are captured
        self.assertEqual(Tags, set(tag_count.keys()), msg="Test needs to capture added tags")

        # Check counts
        expected = {
            COMMENT: 4,
            RBRACE: 25,
            LBRACE: 25,
            WORD: 29,
            XREF: 4,
        }
        for tag, count in expected.items():
            msg = "%s has incorrect count of %d != %d" % (tag, tag_count[tag], count)
            self.assertEqual(count, tag_count[tag], msg=msg)

##########################################################################
## Lexer Test Case
##########################################################################
