# lene.parser
# Parser for LISP representations
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Feb 21 14:37:33 2014 -0500
#
# Copyright (C) 2014 UMD Metacognitive Lab
# For license information, see LICENSE.txt
#
# ID: __init__.py [] bengfort@cs.umd.edu $

"""
Parser for LISP representations
"""

##########################################################################
## Imports
##########################################################################

from .lexer import *
from .tokenize import *
from StringIO import StringIO

##########################################################################
## Module functions
##########################################################################

def load(fp, encoding=None, lexer=None, tokenizer=None, detokenize=True):
    """
    Parse `fp` (a file-like object with a `read` method that contains a
    Lisp document) to a Python object - a list based tree structure.

    If the encoding of the document is anything other than ASCII, the
    encoding needs to be specified.

    If a Lexer other than the one built into this module should be used,
    pass in the class for the Lexer. If a tokenizer other than the one
    built into this module should be used, pass in the class for the
    Tokenizer.

    Finally, if you would like access to the token stream rather than the
    Python primitive objects, set `detokenize` to False.
    """
    lexer  = lexer() if lexer else Lexer()
    stream = TokenStream(fp, tokenizer=tokenizer)
    parse  = lexer.parse(stream)

    if detokenize:
        return list(lexer.detokenize(parse))
    return parse

def loads(s, encoding=None, lexer=None, tokenizer=None, detokenize=True):
    """
    Parse `s` (a string or unicode instance containing a Lisp document) to
    a Python object- a list based tree structure.

    If the encoding of the document is anything other than ASCII, the
    encoding needs to be specified.

    If a Lexer other than the one built into this module should be used,
    pass in the class for the Lexer. If a tokenizer other than the one
    built into this module should be used, pass in the class for the
    Tokenizer.

    Finally, if you would like access to the token stream rather than the
    Python primitive objects, set `detokenize` to False.
    """
    stream = StringIO(s)
    return load(stream, encoding, lexer, tokenizer, detokenize)
