# -*- coding: utf-8 -*-

"""Unit tests for xojo module."""

from __future__ import absolute_import
import pytest
from pygments.token import *
from xojolexer.xojo import XojoLexer

def test_smoke():
    """A basic smoke test."""
    
    assert XojoLexer()



@pytest.mark.parametrize("source, tokens", 
    [
    ('x = 1', [
        (Token.Name.Variable, u'x'),
        (Token.Text, u' '),
        (Token.Operator, u'='),
        (Token.Text, u' '),
        (Token.Literal.Number.Integer, u'1'),
        (Token.Text, u'\n')
        ]),
    
    ])
def test_lexing(source, tokens):    
    lexer = XojoLexer()
    assert [t for t in lexer.get_tokens(source)] == tokens
