# tests.utils_tests.stats_tests
# Test the lene statistics package
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Mar 02 20:26:08 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: stats_tests.py [] bengfort@cs.umd.edu $

"""
Test the lene statistics package
"""

##########################################################################
## Imports
##########################################################################

import unittest
from lene.utils.stats import *

##########################################################################
## Test Cases
##########################################################################

class HistogramTests(unittest.TestCase):

    def test_fromkeys(self):
        """
        Assert from keys classmethod raises NotImplemented
        """
        with self.assertRaises(NotImplementedError):
            h = Histogram.fromkeys([])

    def test_init(self):
        """
        Test instantiation via iterable
        """
        h = Histogram('abcabc')
        for l in 'abc':
            self.assertIn(l, h)
            self.assertEqual(h[l], 2)

    def test_N(self):
        """
        Test population measurement
        """
        h = Histogram('abcabc')
        self.assertEqual(h.N(), 6)

    def test_B(self):
        """
        Test number of bins measurement
        """
        h = Histogram('abcabc')
        self.assertEqual(h.B(), 3)
        self.assertEqual(len(h), h.B())

    def test_freq(self):
        """
        Test the frequency computation
        """
        h = Histogram('abcabcdefa')
        self.assertTrue(isinstance(h.freq('a'), float))
        self.assertEqual(h.freq('a'), 0.3)
        self.assertEqual(h.freq('b'), 0.2)
        self.assertEqual(h.freq('c'), 0.2)
        self.assertEqual(h.freq('d'), 0.1)
        self.assertEqual(h.freq('e'), 0.1)
        self.assertEqual(h.freq('f'), 0.1)

    def test_empty_freq(self):
        """
        Check frequency division by zero edge case
        """
        h = Histogram()
        self.assertEqual(h.freq('a'), 0.0)

    def test_max(self):
        """
        Test the histogram maximum computation
        """
        h = Histogram('abcabcdefa')
        self.assertEqual(h.max(), 'a')

    def test_empty_max(self):
        """
        Assert No KeyError on empty max
        """
        h = Histogram()
        self.assertIsNone(h.max())

    def test_most_commom(self):
        """
        Test the most_common method
        """
        h = Histogram('abcaba')
        self.assertEqual(h.most_common(), [('a', 3), ('b', 2), ('c', 1)])

    def test_n_most_common(self):
        """
        Test n most common items
        """
        h = Histogram('abcabadef')
        self.assertEqual(h.most_common(2), [('a', 3), ('b', 2)])

    def test_empty_most_common(self):
        """
        Test most common on an empty histogram
        """
        h = Histogram()
        self.assertEqual(h.most_common(), [])

    def test_elements(self):
        """
        Test the elements iterable
        """
        h = Histogram('aaaaa')
        self.assertEqual(list(h.elements()), ['a', 'a', 'a', 'a', 'a'])

    def test_update_additive(self):
        """
        Ensure the update method adds rather than replaces.
        """
        h = Histogram('abcaba')
        self.assertEqual(h['a'], 3)
        self.assertEqual(h['b'], 2)
        self.assertEqual(h['c'], 1)

        h.update(Histogram('ab'))
        self.assertEqual(h['a'], 4)
        self.assertEqual(h['b'], 3)
        self.assertEqual(h['c'], 1)

    def test_update_histogram(self):
        """
        Assert can update with a histogram
        """
        h = Histogram('abc')
        self.assertEqual(h['a'], 1)
        self.assertEqual(h['b'], 1)
        self.assertEqual(h['c'], 1)

        h.update(Histogram('abc'))
        self.assertEqual(h['a'], 2)
        self.assertEqual(h['b'], 2)
        self.assertEqual(h['c'], 2)

    def test_update_dictionary(self):
        """
        Assert can update with a dict
        """
        h = Histogram('abc')
        self.assertEqual(h['a'], 1)
        self.assertEqual(h['b'], 1)
        self.assertEqual(h['c'], 1)

        h.update({'a': 1, 'b':1, 'c': 1})
        self.assertEqual(h['a'], 2)
        self.assertEqual(h['b'], 2)
        self.assertEqual(h['c'], 2)

    def test_update_none(self):
        """
        Assert can update with None
        """
        h = Histogram('abc')
        self.assertEqual(h['a'], 1)
        self.assertEqual(h['b'], 1)
        self.assertEqual(h['c'], 1)

        h.update(None)
        self.assertEqual(h['a'], 1)
        self.assertEqual(h['b'], 1)
        self.assertEqual(h['c'], 1)

    def test_update_iterable(self):
        """
        Assert can update with an iterable
        """
        h = Histogram('abc')
        self.assertEqual(h['a'], 1)
        self.assertEqual(h['b'], 1)
        self.assertEqual(h['c'], 1)

        h.update('abc')
        self.assertEqual(h['a'], 2)
        self.assertEqual(h['b'], 2)
        self.assertEqual(h['c'], 2)

    def test_update_kwargs(self):
        """
        Assert can update with kwargs
        """
        h = Histogram('abc')
        self.assertEqual(h['a'], 1)
        self.assertEqual(h['b'], 1)
        self.assertEqual(h['c'], 1)

        h.update(None, a=4)
        self.assertEqual(h['a'], 5)

    def test_incr(self):
        """
        Test increment method
        """
        h = Histogram('abc')
        h.incr('a')
        self.assertEqual(h['a'], 2)
        h.incr('d')
        self.assertEqual(h['d'], 1)
        h.incr('d', 2)
        self.assertEqual(h['d'], 3)

    def test_decr(self):
        """
        Test decr method
        """
        h = Histogram('abcc')
        self.assertEqual(h['a'], 1)
        h.decr('a')
        self.assertEqual(h['a'], 0)
        self.assertNotIn('a', list(h.elements()))

        self.assertEqual(h['c'], 2)
        h.decr('c')
        self.assertEqual(h['c'], 1)
        self.assertIn('c', list(h.elements()))

    def test_copy(self):
        """
        Test the copy method
        """
        h = Histogram('abc')
        h1 = h
        self.assertEqual(id(h1), id(h))
        h2 = h.copy()
        self.assertNotEqual(id(h2), id(h))

    def test_pprint(self):
        """
        Test the pretty print method
        """
        h = Histogram('abc')
        self.assertEqual(h.pprint(), "Histogram({'a': 1, 'c': 1, 'b': 1})")

    def test_long_pprint(self):
        """
        Test pretty print with many elements
        """
        h = Histogram('abcdefghijklmnopqrstuvwxyz')
        self.assertIn('...', h.pprint())

    def test_str(self):
        """
        Test the str method
        """
        h = Histogram('abc')
        self.assertEqual(h.pprint(), str(h))

    def test_repr(self):
        """
        Assert that repr has B and N in it
        """
        h = Histogram('abc')
        self.assertIn(str(h.B()), repr(h))
        self.assertIn(str(h.N()), repr(h))

    def test_del(self):
        """
        Check the del method on Histogram
        """
        h = Histogram('abc')
        self.assertIn('a', h)
        del h['a']
        self.assertNotIn('a', h)

        try:
            del h['a']
        except KeyError:
            self.fail("Delete nonelement should not raise KeyError")

    def test_add(self):
        """
        Test adding two Histograms
        """
        h1 = Histogram('abc')
        h2 = Histogram('ade')
        h3 = h1 + h2

        self.assertIn('a', h3)
        self.assertEqual(h3['a'], 2)

        for l in 'bcde':
            self.assertIn(l, h3)
            self.assertEqual(h3[l], 1)

        # Ensure only histograms can be added
        with self.assertRaises(NotImplementedError):
            h4 = h1 + {'a': 2}

    def test_sub(self):
        """
        Test subtracting two Histograms
        """
        h1 = Histogram('aabc')
        h2 = Histogram('acd')
        h3 = h1 - h2

        self.assertIn('a', h3)
        self.assertEqual(h3['a'], 1)

        for l in 'cd':
            self.assertNotIn(l, h3)

        self.assertIn('b', h3)
        self.assertEqual(h3['b'], 1)

        # Ensure only histograms can be added
        with self.assertRaises(NotImplementedError):
            h4 = h1 - {'a': 2}

    def test_or(self):
        """
        Test maximal union of two Histograms
        """
        h1 = Histogram('aabc')
        h2 = Histogram('abbd')
        h3 = h1 | h2

        for l in 'ab':
            self.assertIn(l, h3)
            self.assertEqual(h3[l], 2)

        for l in 'cd':
            self.assertIn(l, h3)
            self.assertEqual(h3[l], 1)

        # Ensure only histograms can be added
        with self.assertRaises(NotImplementedError):
            h4 = h1 | {'a': 2}

    def test_and(self):
        """
        Test minimal intersection of two Histograms
        """
        h1 = Histogram('aabcc')
        h2 = Histogram('abbdd')
        h3 = h1 & h2

        for l in 'ab':
            self.assertIn(l, h3)
            self.assertEqual(h3[l], 1)

        for l in 'cd':
            self.assertNotIn(l, h3)

        # Ensure only histograms can be added
        with self.assertRaises(NotImplementedError):
            h4 = h1 & {'a': 2}

    def test_and_varied_lenght(self):
        """
        Test intersection of varied length histograms
        """

        h1 = Histogram('aabcc')
        h2 = Histogram('abbdefg')
        h3 = h1 & h2
        h4 = h2 & h1

        self.assertEqual(h3, h4)

class TokenFrequencyTests(unittest.TestCase):

    def test_from_tree(self):
        """
        Assert a token frequency construction from tree
        """
        tree = ['a', ['b', ['c', 'd'], 'e'], ['f', ['g', ['h'], ['i', ['j']]]]]
        freq = TokenFrequency.from_tree(tree, idxmax=10) # idxmax to ensure capture

        for i in xrange(0,5):
            self.assertIn(i, freq)

        levels = (
            ('a',),
            ('b', 'e', 'f'),
            ('c', 'd', 'g'),
            ('i', 'h'),
            ('j', )
        )

        for idx, chars in enumerate(levels):
            for char in chars:
                self.assertIn(char, freq[idx])
                self.assertEqual(1, freq[idx][char])

    def test_from_tree_idx_max(self):
        """
        Assert frequency construction with idx max
        """
        tree = ['a', ['b', ['c', 'd'], 'e'], ['f', ['g', ['h'], ['i', ['j']]]]]
        freq = TokenFrequency.from_tree(tree, idxmax=0) # idxmax to filter

        for i in xrange(0,5):
            self.assertIn(i, freq)

        levels = (
            ('a',),
            ('b', 'f'),
            ('c', 'g'),
            ('i', 'h'),
            ('j', )
        )

        for idx, chars in enumerate(levels):
            for char in chars:
                self.assertIn(char, freq[idx])
                self.assertEqual(1, freq[idx][char])

    def test_update(self):
        """
        Test updating of two token frequencies
        """
        tree = ['a', ['b', ['c', 'd'], 'e'], ['f', ['g', ['h'], ['i', ['j']]]]]
        alph = TokenFrequency.from_tree(tree, idxmax=3)
        beth = TokenFrequency.from_tree(tree, idxmax=3)

        alph.update(beth)
        for i in xrange(0,5):
            self.assertIn(i, alph)

        levels = (
            ('a',),
            ('b', 'e', 'f'),
            ('c', 'd', 'g'),
            ('i', 'h'),
            ('j', )
        )

        for idx, chars in enumerate(levels):
            for char in chars:
                self.assertIn(char, alph[idx])
                self.assertEqual(2, alph[idx][char])

    def test_string_reps(self):
        """
        Exercise the string methods of TokenFrequency
        """
        tree = ['a', ['b', ['c', 'd'], 'e'], ['f', ['g', ['h'], ['i', ['j']]]]]
        freq = TokenFrequency.from_tree(tree)

        try:
            tstr = str(freq)
            trpr = repr(freq)
        except Exception as e:
            self.fail(str(e))
