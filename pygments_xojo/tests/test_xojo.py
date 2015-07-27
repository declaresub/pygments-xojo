# -*- coding: utf-8 -*-

"""Unit tests for xojo module."""

from __future__ import absolute_import
import re
import pytest
from pygments.token import *
from pygments_xojo.xojo import XojoLexer

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
        ]),

    ('class Foo', [
        (Token.Keyword.Reserved, u'class'),
        (Token.Text, u' '),
        (Name.Class, u'Foo'), 
        ]),
        
    ('function Foo', [
        (Token.Keyword.Reserved, u'function'),
        (Token.Text, u' '),
        (Name.Function, u'Foo'), 
        ]),
         
     ('sub Foo', [
        (Token.Keyword.Reserved, u'sub'),
        (Token.Text, u' '),
        (Name.Function, u'Foo'), 
        ]),

    ('x as Ptr', [
        (Name.Variable, u'x'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name.XojoType, u'Ptr'),
        ]),

    ('x as Ptr, s as String', [
        (Name.Variable, u'x'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name.XojoType, u'Ptr'),
        (Punctuation, u','),
        (Token.Text, u' '),
        (Name.Variable, u's'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name.XojoType, u'String'),        
        ]),

    ('soft declare sub foo lib "Bar" ()', [
        (Keyword.Declaration, u'soft'), 
        (Token.Text, u' '), 
        (Keyword.Declaration, u'declare'), 
        (Token.Text, u' '), 
        (Keyword.Reserved, u'sub'), 
        (Token.Text, u' '), 
        (Name.Function, u'foo'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'lib'), 
        (Token.Text, u' '),
        (String, u'"Bar"'),     
        (Token.Text, u' '),
        (Punctuation, u'('),
        (Punctuation, u')'),
        ]),
                    
    ('declare function foo lib "Bar" () as String', [
        (Keyword.Declaration, u'declare'),
        (Text, u' '),
        (Keyword.Reserved, u'function'),
        (Text, u' '),
        (Name.Function, u'foo'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'lib'), 
        (Token.Text, u' '),
        (String, u'"Bar"'),     
        (Token.Text, u' '),
        (Punctuation, u'('),
        (Punctuation, u')'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Token.Text, u' '),
        (Token.Name.XojoType, u'String'),        
        ]),

    ('declare sub setValue lib AppKit.framework selector "setValue" (this as Ptr, value as Integer)', [
        (Keyword.Declaration, u'declare'), 
        (Token.Text, u' '),
        (Keyword.Reserved, u'sub'), 
        (Token.Text, u' '),
        (Name.Function, u'setValue'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'lib'), 
        (Token.Text, u' '),
        (Token.Name, u'AppKit.framework'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'selector'),
        (Token.Text, u' '),
        (String, u'"setValue"'), 
        (Token.Text, u' '),
        (Punctuation, u'('),
        (Name.Variable, u'this'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name.XojoType, u'Ptr'),
        (Punctuation, u','),
        (Token.Text, u' '),
        (Name.Variable, u'value'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Text, u' '),
        (Name.XojoType, u'Integer'),        
        (Punctuation, u')'),
        ]),  
            
    #alias is a keyword only inside a declare statement. 
    ('dim alias as String = f.Alias', [
        (Token.Keyword.Declaration, u'dim'),
        (Token.Text, u' '),
        (Token.Name.Variable, u'alias'),
        (Token.Text, u' '),
        (Keyword.Reserved, u'as'),
        (Token.Text, u' '),
        (Token.Name.XojoType, u'String'),  
        (Token.Text, u' '),        
        (Token.Operator, u'='),
        (Token.Text, u' '), 
        (Name.Variable, u'f'),
        (Punctuation, u'.'),
        (Name.Variable, u'Alias'),
        ]),
        
    ('dim _\n_x _ //comment\nas_\nString', [
        (Keyword.Declaration, u'dim'),
        (Text, u' '),
        (Punctuation, u'_'),
        (Text, u'\n'),
        (Name.Variable, u'_x'),
        (Text, u' '),
        (Punctuation, u'_'),
        (Text, u' '),
        (Comment, u'//comment'),
        (Text, u'\n'),
        (Name.Variable, u'as_'),
        (Text, u'\n'),
        (Name.Variable, u'String'),
        ]),
    ])
def test_lexing(source, tokens):    
    lexer = XojoLexer()
    for t in lexer.get_tokens(source):
        print(t)
    assert [t for t in lexer.get_tokens(source)] == tokens
