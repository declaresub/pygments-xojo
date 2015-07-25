# -*- coding: utf-8 -*-

"""Unit tests for xojo module."""

from __future__ import absolute_import
import pytest
from pygments.token import *
from xojolexer.xojo import XojoLexer, _FunctionParamsLexer

def test_smoke():
    """A basic smoke test."""
    
    assert XojoLexer()



@pytest.mark.parametrize("source, tokens", 
    [
    ('x as Ptr', [
        (Name.Variable, u'x'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name, u'Ptr'),
        (Token.Text, u'\n')
        ]),

    ('x as Ptr, s as String', [
        (Name.Variable, u'x'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name, u'Ptr'),
        (Punctuation, u','),
        (Token.Text, u' '),
        (Name.Variable, u's'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name, u'String'),        
        (Token.Text, u'\n')
        ]),
            
    ])
def test_function_args(source, tokens):
    lexer = _FunctionParamsLexer()
    assert [t for t in lexer.get_tokens(source)] == tokens
    





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
