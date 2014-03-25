# lene.utils.stats
# Provides a statistical analysis of tokens
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Feb 27 10:58:35 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: stats.py [] bengfort@cs.umd.edu $

"""
Provides a statistical analysis of tokens
"""

##########################################################################
## Imports
##########################################################################

from heapq import nlargest
from operator import itemgetter
from lene.utils import walk, flatten
from itertools import repeat, ifilter

##########################################################################
## Evaluation Classes
##########################################################################

class Histogram(dict):
    """
    Dict subclass for counting hashable objects, sometimes called a Bag or
    a multiset. Elements are stored as dictionary keys and thier frequency
    is stored as dictionary values. Various probabilities can be computed
    as this class represents a frequency distribution.

    See `collections.Counter` for an example of this in the Python stdlib.
    This class is implemented here to provide support for Python < 2.7.

    >>> Histogram('abbabcddc')
    Histogram({'a':2, 'b':3, 'c':2, 'd':2})
    """

    @classmethod
    def fromkeys(klass, iterable, v=None):
        raise NotImplementedError(
            "Histogram.fromkeys() is undefined. Use Histogram(iterable)."
        )

    def __init__(self, iterable=None, **kwargs):
        """
        Create a new, empty Histogram. If an iterable is given, then count
        the elements of the iterable, or initialize the counts from
        another Histogram.
        """
        self.update(iterable, **kwargs)

    def N(self):
        """
        Total number of tokens/samples
        """
        return sum(self.values())

    def B(self):
        """
        Return total number of sample values or bins that have a frequency
        greater than zero. Histogram.B() is the same as len(Histogram).
        """
        return len(self)

    def freq(self, elem):
        """
        Return the frequency of the given element. The frequency of the
        element is the count of the element divided by the total number
        of sample outcomes that have been recorded. Frequencies are always
        real numbers in the range [0, 1].
        """
        if self.N() == 0:
            return 0.0
        return float(self[elem]) / self.N()

    def max(self):
        """
        Return the element with the highest frequency. If two elements
        have the same frequency, one of them is returned.
        """
        if len(self) == 0:
            return None
        return self.most_common(1)[0][0]

    def most_common(self, n=None):
        """
        List the n most common elements and their frequencies from the
        most common to the least common. If n is None, then list all
        frequencies.
        """
        if n is None:
            return sorted(self.iteritems(), key=itemgetter(1), reverse=True)
        return nlargest(n, self.iteritems(), key=itemgetter(1))

    def elements(self):
        """
        Iterate over elements repeating as many times as its frequency
        """
        for elem, count in self.iteritems():
            for _ in repeat(None, count):
                yield elem

    def update(self, iterable=None, **kwargs):
        """
        Like dict.update but adds frequencies instead of replacing them.

        Source can be an iterable, a dictionary, or another Histogram
        """
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    dict.update(self, iterable) # Faster if empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1

        if kwargs:
            self.update(kwargs)

    def incr(self, elem, n=1):
        """
        Increment an element
        """
        self[elem] += n

    def decr(self, elem, n=1):
        """
        Decrement an element, floor is zero
        """
        newcount = self[elem] - n
        if newcount > 0:
            self[elem] = newcount
        else:
            del self[elem]

    def copy(self):
        """
        like dict.copy() but returns a Histogram instead of a dict.
        """
        return Histogram(self)

    def __missing__(self, key):
        """
        Returns the default value when requested key is not found.
        """
        return 0

    def pprint(self, maxlen=10):
        """
        Return a string representation of this Histogram.

        :param maxlen: The maximum number of items to display
        :type maxlen: int
        :rtype: string
        """
        items = ['{0!r}: {1!r}'.format(*item) for item in self.most_common(maxlen)]
        if len(self) > maxlen:
            items.append('...')
        return 'Histogram({{{0}}})'.format(', '.join(items))

    def __str__(self):
        """
        Return a string representation of this Histogram.

        :rtype: string
        """
        return self.pprint()

    def __repr__(self):
        return '<Histogram with %d samples and %d outcomes>' % (len(self), self.N())

    def __delitem__(self, elem):
        """
        like dict.__delitem__ but does not raise KeyError
        """
        if elem in self:
            dict.__delitem__(self, elem)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += Counter()

    def __add__(self, other):
        """
        Adds frequencies from two Histograms
        """
        if not isinstance(other, Histogram):
            raise NotImplementedError()
        result = Histogram()
        for elem in set(self) | set(other):
            newcount = self[elem] + other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __sub__(self, other):
        """
        Subtracts frequencies but only allows positive results
        """
        if not isinstance(other, Histogram):
            raise NotImplementedError()
        result = Histogram()
        for elem in set(self) | set(other):
            newcount = self[elem] - other[elem]
            if newcount > 0:
                result[elem] = newcount
        return result

    def __or__(self, other):
        """
        Union, selects maximum in either Histogram
        """
        if not isinstance(other, Histogram):
            raise NotImplementedError()
        _max = max
        result = Histogram()
        for elem in set(self) | set(other):
            newcount = _max(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result

    def __and__(self, other):
        """
        Intersection is minimum of either Histogram
        """
        if not isinstance(other, Histogram):
            raise NotImplementedError()
        _min = min
        result = Histogram()
        if len(self) < len(other):
            self, other = other, self
        for elem in ifilter(self.__contains__, other):
            newcount = _min(self[elem], other[elem])
            if newcount > 0:
                result[elem] = newcount
        return result


class TokenFrequency(dict):
    """
    Evaluates the frequency of tokens at each depth of a Tree - e.g. a
    data structure that contains a Histogram at each depth of the various
    levels of the Tree.
    """

    @classmethod
    def from_tree(klass, tree, idxmax=0):
        """
        To do, deal with tokens of greater index mass
        """
        tokens = klass()
        for idx, token, depth in walk(tree):
            if idx > idxmax: continue
            tokens[depth][token] += 1
        return tokens

    def __init__(self, tree=None, **kwargs):
        """
        Initialize a HierarchyHistogram from a Tree
        """
        self.update(tree, **kwargs)

    def __missing__(self, key):
        self[key] = Histogram()
        return Histogram()

    def update(self, iterable=None, **kwargs):
        """
        Updates Histogram at each depth of the iterable, which should be
        a Tree-like, hierarchical data structure.
        """
        if iterable is not None:
            if hasattr(iterable, 'iteritems'):
                if self:
                    for elem, hist in iterable.iteritems():
                        self[elem].update(hist)
                else:
                    dict.update(self, iterable)
            else:
                for idx, elem, depth in walk(iterable):
                    self[depth][elem] += 1
        if kwargs:
            self.update(kwargs)

    def pprint(self, depth=None):
        """
        Pretty prints the token frequencies at each level of the tree.
        """
        # Get the levels to print out, stopping at particular depth
        levels = sorted(self.keys())
        if depth: levels = levels[:depth]

        # Build output with the levels
        output = []
        for level in levels:
            # Create Header for this depth
            output.append("Tree Level %i" % level)
            output.append("=" * len(output[-1]))

            # Create frequencies of the most common tokend
            for token, count in self[level].most_common():
                output.append("  {0: <4} {1}".format(count, token))

            # Create space between tree levels
            output.append("")

        return "\n".join(output)

    def __repr__(self):
        samples  = sum(len(d) for d in self.values())
        outcomes = sum(d.N() for d in self.values())
        output   = '<TokenFrequency Tree with %d levels and %d outcomes in %d samples>'
        return output % (len(self), samples, outcomes)

    def __str__(self):
        return self.pprint()
