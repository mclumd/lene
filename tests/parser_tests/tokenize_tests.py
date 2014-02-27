# tests.parser_tests.tokenize_tests
# Testing the tokenization module
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 10:15:07 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: tokenize_tests.py [] bengfort@cs.umd.edu $

"""
Testing the tokenization module
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest
import tempfile

from lene.parser.tokenize import *
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
## Lisp-like fixture
##########################################################################

simple_fixture = """
(define-frame BURNS
  (isa (value (violent-mop)))
  (actor
    (value (non-volitional-agent)))
  (object
    (value (physical-object)))
)"""

fixture = """
(in-package :reps)

;;; The BURNS frame
(define-frame BURNS
          (isa (value (violent-mop)))
  (actor
    (value (non-volitional-agent)))
  (object
    (value (physical-object)))
  (goal-scene
    (value (ingest->fuel
         (actor
           (value =actor)); Same actor as above
         (object
           (value =object)) ; Same object as above
         )))
  (scenes
    (value (=goal-scene))); The scene is the goal scene
  (main-result
    (value (burning?
         (domain (value =object))
         )))
  )
(define area (lambda (r) (* 3.14 (* r r))))
"""

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

    def test_unexpected_character(self):
        """
        Assure unexpected characters raise exceptions
        """
        tokenizer = Tokenizer()
        with self.assertRaises(UnexpectedCharacter):
            token = list(tokenizer.tokenize('$!@#%!#(!@#$~~SDVASF'))

    def test_keywords(self):
        """
        Check that keywords come out as tags
        """
        tokenizer = Tokenizer(keywords={'IF', 'ELSE', 'THEN'})
        token = list(tokenizer.tokenize('IF a THEN b ELSE c'))
        self.assertEqual(token[0].tag, 'IF')
        self.assertEqual(token[2].tag, 'THEN')
        self.assertEqual(token[4].tag, 'ELSE')

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
        tokenizer = Tokenizer()
        tokens = list(tokenizer.tokenize(fixture))
        self.assertEqual(len(tokens), 106)

        # Count the various tags
        tag_count = defaultdict(int)
        for token in tokens:
            tag_count[token.tag] += 1

        # Ensure that all tags are captured
        self.assertEqual(Tags, set(tag_count.keys()), msg="Test needs to capture added tags")

        # Check counts
        expected = {
            COMMENT: 4,
            RBRACE: 31,
            LBRACE: 31,
            WORD: 32,
            XREF: 5,
            NUMBER: 1,
            OPERAT: 2,
        }
        for tag, count in expected.items():
            msg = "%s has incorrect count of %d != %d" % (tag, tag_count[tag], count)
            self.assertEqual(count, tag_count[tag], msg=msg)

##########################################################################
## Lene Tokens Test Case
##########################################################################

class LeneTokensTest(unittest.TestCase):
    """
    Test the default tokens mapped in the Tokenizer specification.
    """

    def setUp(self):
        self.tokenizer = Tokenizer()

    def assertTag(self, token, tag, msg=None):
        """
        Assert that a token contains a particular tag.
        If token is a basestring, tokenize and test first token.
        """
        if isinstance(token, basestring):
            token = list(self.tokenizer.tokenize(token))[0]
        self.assertTrue(isinstance(token, Token))
        self.assertEqual(token.tag, tag, msg=msg)

    def assertNotTag(self, token, tag, msg=None):
        """
        Assert that a token does not contain a particular tag.
        If token is a basestring, tokenize and test firt token.

        Note: does not handle UnexpectedCharacter exceptions.
        """
        if isinstance(token, basestring):
            token = list(self.tokenizer.tokenize(token))[0]
        self.assertTrue(isinstance(token, Token))
        self.assertNotEqual(token.tag, tag, msg=msg)

    def assertValidTags(self, tokens, tag, msg=None):
        """
        Assert that a list of tokens is a valid tag.
        """
        for token in tokens:
            self.assertTag(token, tag, msg=msg)

    def assertInvalidTags(self, tokens, tag, msg=None):
        """
        Assert that a list of tokens is not a valid tag.
        """
        for token in tokens:
            self.assertNotTag(token, tag, msg=msg)

    def test_rbrace(self):
        """
        Test RBRACE token
        """
        valid   = ["(", " ( ", "( "]
        invalid = [")", '1', 'abc', ")("]

        self.assertValidTags(valid, RBRACE)
        self.assertInvalidTags(invalid, RBRACE)

    def test_lbrace(self):
        """
        Test LBRACE token
        """
        valid   = [")", " ) ", ") "]
        invalid = ["(", '1', 'abc', "()"]

        self.assertValidTags(valid, LBRACE)
        self.assertInvalidTags(invalid, LBRACE)

    def test_comment(self):
        """
        Test COMMENT token

        Note: Comments must have newlines?
        """
        valid   = [";\n", ";; Bob was here\n", ";comment\n"]
        invalid = ["); comment\n", "words\n", "2.324\n"]

        self.assertValidTags(valid, COMMENT)
        self.assertInvalidTags(invalid, COMMENT)

    def test_word(self):
        """
        Test WORD token
        """
        valid   = ['abc', 'define-frame', '_var', 'flight123', 'actor.0',
                   'lady_bug', 'ladyBug', 'LADYBUG', 'LadyBug', '__var',
                   'define->actor', 'list?', 'actor<-me']
        invalid = ['-joe', '123flight', '0.3', '.3', '(word)', '+joe']

        self.assertValidTags(valid, WORD)
        self.assertInvalidTags(invalid, WORD)

    def test_xref(self):
        """
        Test XREF token
        """
        valid   = ['=actor', '=a123', '=_14', ":reps", ":_reps"]
        invalid = ['a=b', '-=a', 'foo', '1.23']

        self.assertValidTags(valid, XREF)
        self.assertInvalidTags(invalid, XREF)

    def test_number(self):
        """
        Test NUMBER token

        Note: 1x1 and 1e10 becomes 2 tokens NUMBER, WORD
        """
        valid   = ['0.3', '-3', '+4', '.832', '14091.313', '23', '-0.23', '+0.24']
        invalid = ['a.3', 'zing', '(3)', ';3.0\n']

        self.assertValidTags(valid, NUMBER)
        self.assertInvalidTags(invalid, NUMBER)

    def test_operat(self):
        """
        Test OPERAT token
        """
        valid   = ['+', '-', '*', '/', '%']
        invalid = ['+3', '-4', 'abc', '3/4']

        self.assertValidTags(valid, OPERAT)
        self.assertInvalidTags(invalid, OPERAT)

##########################################################################
## TokenStream Test Case
##########################################################################

class TokenStreamTest(unittest.TestCase):

    def setUp(self):
        """
        Setup temporary file as fixture.
        """
        hndl, path = tempfile.mkstemp(suffix='.lisp', prefix='representation-')
        self.temppath = path
        with open(path, 'w') as lispy:
            lispy.write(fixture)

    def tearDown(self):
        """
        Ensure remove of tempfile
        """
        if os.path.exists(self.temppath):
            os.remove(self.temppath)
        self.assertFalse(os.path.exists(self.temppath))

    def test_open_stream(self):
        """
        Check tokenization on stream
        """
        stream = TokenStream(open(self.temppath, 'r'))
        self.assertEqual(len(list(stream)), 106)

    def test_path_stream(self):
        """
        Check pass path to stream
        """
        stream = TokenStream(self.temppath)
        self.assertEqual(len(list(stream)), 106)
