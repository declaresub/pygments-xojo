# -*- coding: utf-8 -*-
"""
pygments.lexers.basic
~~~~~~~~~~~~~~~~~~~~~

Lexer for the Xojo language.

:copyright: Copyright 2015 Charles Yeomans.
:license: BSD, see LICENSE for details.
"""

from __future__ import absolute_import
import re
from pygments.lexer import RegexLexer, words, include
from pygments.token import Keyword, Name, String, Literal, Number, Punctuation, Comment, \
    Operator, Text

__all__ = ['XojoLexer']

class XojoLexer(RegexLexer):
    """Lexer for Xojo."""

    name = 'xojo'
    aliases = ['xojo']
    flags = re.IGNORECASE | re.UNICODE

    #pylint: disable=bad-continuation
    IDENTIFIER = r'[^\d\W]\w*'
    BUILTINS = ('AddHandler', 'Call','CurrentMethodName',
    'Raise',  'RemoveHandler')
    KEYWORDS = ('Aggregates', 'As', 'Assigns', 'Attributes', 'Break', 'ByRef', 'ByVal',
    'Case', 'Catch', 'Class', 'Continue', 'Declare', 'Delegate', 'Do', 'DownTo', 'Each',
    'Enum', 'Else', 'ElseIf', 'End', 'Event', 'Exception', 'Exit', 'Extends', 'Finally',
    'For', 'Function', 'Global', 'Handles', 'If', 'Implements', 'In', 'Inherits', 'Interface',
    'Lib', 'Loop', 'Module', 'Next', 'New', 'Namespace', 'Optional', 'ParamArray', 'Private',
    'Protected', 'Public', 'Return', 'Select', 'Selector', 'Soft', 'Step', 'Structure',
    'Sub', 'Then', 'To', 'Try', 'Until', 'Wend', 'While', 'With', 'WithEvents',
    '#if', '#else', '#endif', '#pragma')
    OPERATOR_WORDS = ('And', 'Is', 'IsA', 'Mod', 'Not', 'Or', 'Xor', 'AddressOf', 'Array',
    'Ctype', 'GetTypeInfo', 'RaiseEvent', 'Redim', 'WeakAddressOf')
    
    tokens = {
        'ignorable_whitespace': [
            (r'[\ \t]+', Text),
            ],
            
        'root': [
            include('ignorable_whitespace'),
            (words(('const', 'dim', 'static'), suffix=r'\b'), Keyword.Declaration),
            (words(('false', 'nil', 'true'), suffix=r'\b'), Keyword.Constant),
            (words(BUILTINS, suffix=r'\b'), Name.Builtin),
            (words(('Using',), suffix=r'\b'), Keyword.Namespace, 'using_ns'),
            (words(('GOTO',), suffix=r'\b'), Keyword.Reserved, 'goto'),
            (words(('self', 'me', 'super'), suffix=r'\b'), Name.Builtin.Pseudo),
            (words(KEYWORDS, suffix=r'\b'), Keyword.Reserved),

            # Literals
            (r'"(""|[^"])*"', String),
            (r'&u[0-9a-fA-F]+', Literal),
            (r'[0-9]+', Number.Integer),
            (r'&b[01]+', Number.Bin),
            (r'&o[0-7]+', Number.Oct),
            (r'&h[0-9a-fA-F]+', Number.Hex),
            (r'&c[0-9a-fA-F]{8}', Literal),
            (r'&c[0-9a-fA-F]{6}', Literal),

            # line continuation
            (r'_(?!\w)', Punctuation),
            (r"\'.*", Comment),
            (r'//.*', Comment),
            (r'REM\b.*', Comment),

            (r'(<=?)|(>=?)|(<>)|[\=\+\-\*/\^\<\>]', Operator),
            (words(OPERATOR_WORDS, prefix=r'\b', suffix=r'\b'), Operator.Word),
            (r'[(),.:]', Punctuation),
            (r'[^\d\W]\w*:', Name.Label),
            (IDENTIFIER, Name.Variable),
            ],

        'using_ns': [
            include('ignorable_whitespace'),
            (r'[^\d\W]\w*(.[^\d\W]\w*)*', Name.Namespace, '#pop'),
            ],

        'goto': [
            include('ignorable_whitespace'),
            (IDENTIFIER, Name.Label, '#pop'),
            ],
        }
