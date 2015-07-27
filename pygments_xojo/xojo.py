# -*- coding: utf-8 -*-
"""
Lexer for the Xojo language.

:copyright: Copyright 2015 Charles Yeomans.
:license: BSD, see LICENSE for details.
"""

from __future__ import absolute_import
import re
from pygments.lexer import RegexLexer, words, include, default
from pygments.token import Keyword, Name, String, Literal, Number, Punctuation, Comment, \
    Operator, Text


__all__ = ['XojoLexer']


# various regular expressions
IDENTIFIER = r'[^\d\W]\w*'
IDENTIFIER_FQ = r'[^\d\W]\w*(\.[^\d\W]\w*)*'
LITERAL_STRING = r'"(""|[^"])*"'
LITERAL_UNICODE = r'&u[0-9a-fA-F]+'
WHITESPACE = r'[\ \t]+'
LITERAL_COLOR_32 = r'&c[0-9a-fA-F]{8}'
LITERAL_COLOR_24 = r'&c[0-9a-fA-F]{6}'
DECLARE = r'(soft\s+)?declare[^)]+\)'
WORD_SUFFIX = r'\b'

#pylint: disable=too-few-public-methods
class _LexerOptionsMixin(object):
    """Sets lexer options for Xojo."""

    def __init__(self, *args, **kwargs):
        kwargs['ensurenl'] = False
        super(_LexerOptionsMixin, self).__init__(*args, **kwargs)

class XojoLexer(_LexerOptionsMixin, RegexLexer):
    """Lexer for Xojo."""

    name = 'xojo'
    aliases = ['xojo']
    flags = re.IGNORECASE | re.UNICODE

    #pylint: disable=bad-continuation
    CONSTANTS = ['false', 'nil', 'true']
    DECLARATIONS = ['const', 'dim', 'static', 'soft']
    PSEUDO_BUILTINS = ['self', 'me', 'super']
    BUILTINS = ['AddHandler', 'Call', 'CurrentMethodName',
    'Raise', 'RemoveHandler']
    KEYWORDS = ['Aggregates', 'Assigns', 'Attributes', 'Break', 'ByRef', 'ByVal',
    'Case', 'Catch', 'Class', 'Continue', 'Delegate', 'Do', 'DownTo', 'Each',
    'Enum', 'Else', 'ElseIf', 'End', 'Event', 'Exception', 'Exit', 'Extends', 'Finally',
    'For', 'Function', 'Global', 'Handles', 'If', 'Implements', 'In', 'Inherits', 'Interface',
    'Lib', 'Loop', 'Module', 'Next', 'New', 'Namespace', 'Optional', 'ParamArray', 'Private',
    'Protected', 'Public', 'Return', 'Select', 'Selector', 'Soft', 'Step', 'Structure',
    'Sub', 'Then', 'To', 'Try', 'Until', 'Wend', 'While', 'With', 'WithEvents',
    '#if', '#else', '#endif', '#pragma']
    OPERATOR_WORDS = ['And', 'Is', 'IsA', 'Mod', 'Not', 'Or', 'Xor', 'AddressOf', 'Array',
    'Ctype', 'GetTypeInfo', 'RaiseEvent', 'Redim', 'WeakAddressOf']

    tokens = {
        'whitespace': [
            (r'[\ \t]+', Text),
            ],

        'function_decl': [
            (words(['function', 'sub'], suffix=r'\b'), Keyword.Reserved, 'function_name'),
                ],

        'root': [
            include('whitespace'),
            (words(DECLARATIONS, suffix=WORD_SUFFIX), Keyword.Declaration),
            (words(CONSTANTS, suffix=WORD_SUFFIX), Keyword.Constant),
            (words(PSEUDO_BUILTINS, suffix=WORD_SUFFIX), Name.Builtin.Pseudo),
            (words(('Using', 'module'), suffix=WORD_SUFFIX), Keyword.Namespace, 'namespace_name'),
            (words(['class'], suffix=WORD_SUFFIX), Keyword.Reserved, 'class_name'),
            include('function_decl'),
            (words(['as'], suffix=WORD_SUFFIX), Keyword.Reserved, 'as'),
            (words(['declare'], suffix=WORD_SUFFIX), Keyword.Declaration, 'declare'),
            (words(['GOTO'], suffix=WORD_SUFFIX), Keyword.Reserved, 'goto'),
            (words(BUILTINS, suffix=WORD_SUFFIX), Name.Builtin),
            (words(KEYWORDS, suffix=WORD_SUFFIX), Keyword.Reserved),

            # Literals
            (LITERAL_STRING, String),
            (LITERAL_UNICODE, Literal),
            (r'[0-9]+', Number.Integer),
            (r'&b[01]+', Number.Bin),
            (r'&o[0-7]+', Number.Oct),
            (r'&h[0-9a-fA-F]+', Number.Hex),
            (LITERAL_COLOR_32, Literal),
            (LITERAL_COLOR_24, Literal),

            # line continuation
            (r'_(?!\w)', Punctuation),
            (r"\'.*", Comment),
            (r'//.*', Comment),
            (r'REM\b.*', Comment),

            (r'<>|<=?|>=?|[-=+*/^]', Operator),
            (words(OPERATOR_WORDS, suffix=WORD_SUFFIX), Operator.Word),
            (r'[(),.:]', Punctuation),
            (r'[^\d\W]\w*:', Name.Label),
            (IDENTIFIER, Name.Variable),
            ],

        'namespace_name': [
            include('whitespace'),
            (r'[^\d\W]\w*(.[^\d\W]\w*)*', Name.Namespace, '#pop'),
            ],

         'class_name': [
            include('whitespace'),
            (IDENTIFIER, Name.Class, '#pop'),
            ],

        'function_name': [
            include('whitespace'),
            (IDENTIFIER, Name.Function, '#pop'),
            ],

        'declare': [
            include('whitespace'),
            include('function_decl'),
            (words(['lib'], suffix=WORD_SUFFIX), Keyword.Reserved, 'declare_lib_name'),
            (words(['alias, selector'], suffix=WORD_SUFFIX), Keyword.Reserved,
                'declare_alias_name'),
            default('#pop'),
            ],

        'declare_lib_name': [
            include('whitespace'),
            (LITERAL_STRING, String, '#pop'),
            (LITERAL_UNICODE, Literal, '#pop'),
            (IDENTIFIER_FQ, Name, '#pop'),
            ],

        'declare_alias_name': [
            include('whitespace'),
            (LITERAL_STRING, String, '#pop'),
            (LITERAL_UNICODE, Literal, '#pop'),
            ],

        'goto': [
            include('whitespace'),
            (IDENTIFIER, Name.Label, '#pop'),
            ],

        'as': [
            include('whitespace'),
            (IDENTIFIER, Name.XojoType, '#pop'),
            ],
        }
