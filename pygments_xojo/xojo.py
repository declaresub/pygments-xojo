# -*- coding: utf-8 -*-
"""
Lexer for the Xojo language.

:copyright: Copyright 2015 Charles Yeomans.
:license: BSD, see LICENSE for details.
"""

from __future__ import absolute_import
import re
from pygments.lexer import RegexLexer, words, include, default, using
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

#pylint: disable=too-few-public-methods
class _LexerOptionsMixin(object):
    """Sets lexer options for Xojo."""

    def __init__(self, *args, **kwargs):
        kwargs['ensurenl'] = False
        super(_LexerOptionsMixin, self).__init__(*args, **kwargs)

class _FunctionParamsLexer(_LexerOptionsMixin, RegexLexer):
    """An internal lexer for function parameters."""

    name = 'xojofunctionparam'
    aliases = ['xojofunctionparam']
    flags = re.IGNORECASE | re.UNICODE

    PARAM_NAME = IDENTIFIER
    PARAM_AS = r'as'
    PARAM_TYPE = IDENTIFIER
    PARAM_SEP = r'\,'


    tokens = {
        'ignorable_whitespace': [
            (WHITESPACE, Text),
            ],

        'root': [
            include('ignorable_whitespace'),
            (PARAM_NAME, Name.Variable, 'param_as'),
            ],

        'param_as': [
            include('ignorable_whitespace'),
            (PARAM_AS, Keyword.Reserved, 'param_type')
            ],

        'param_type': [
            include('ignorable_whitespace'),
            (PARAM_TYPE, Name.XojoType, 'param_sep'),
            ],

        'param_sep': [
            include('ignorable_whitespace'),
            (PARAM_SEP, Punctuation, 'root'),
            default('#pop'),
            ],
        }

class _DeclareLexer(_LexerOptionsMixin, RegexLexer):
    """Internal lexer for declare statements.  Note that for function declares, the
    'as Typename' bit is handled by XojoLexer."""

    name = 'xojodeclaresub'
    aliases = ['xojodeclaresub']
    flags = re.IGNORECASE | re.UNICODE

    DECLARE_DECL = r'(soft\s+)?declare\s+(function|sub)'
    DECLARE_FUNCTION_NAME = IDENTIFIER
    DECLARE_FUNCTION_ARGS = r'[^)]*'
    DECLARE_LIB = r'lib'
    DECLARE_ALIAS = 'r(alias)|(selector)'

    tokens = {
        'root': [
            (r'[\ ]+', Text),
            (DECLARE_DECL, Keyword.Reserved, 'declare_function_name'),
            ],

        'whitespace': [
            (WHITESPACE, Text),
            ],

        'declare_function_name': [
            (r'[\ ]+', Text),
            (DECLARE_FUNCTION_NAME, Name.Function, 'declare_lib'),
            ],

        'declare_lib': [
            include('whitespace'),
            (DECLARE_LIB, Keyword.Reserved, 'declare_lib_name')
            ],

        'declare_lib_name': [
            include('whitespace'),
            (LITERAL_STRING, String, 'declare_alias'),
            (LITERAL_UNICODE, Literal, 'declare_alias'),
            (IDENTIFIER_FQ, Name, 'declare_alias'),
            ],

        'declare_alias': [
            include('whitespace'),
            (DECLARE_ALIAS, Keyword, 'declare_alias_name'),
            default('declare_function_args_start')
            ],

        'declare_alias_name': [
            include('whitespace'),
            (LITERAL_STRING, String, 'declare_function_args_start'),
            (LITERAL_UNICODE, Literal, 'declare_function_args_start'),
            ],

        'declare_function_args_start': [
            (r'\ +', Text),
            (r'\(', Punctuation, 'declare_function_args'),
            ],

        'declare_function_args': [
            (r'\ +', Text),
            (DECLARE_FUNCTION_ARGS, using(_FunctionParamsLexer), 'declare_function_args_end')
            ],

        'declare_function_args_end': [
            (r'\ +', Text),
            (r'\)', Punctuation, 'root'),
            ],
        }

class XojoLexer(_LexerOptionsMixin, RegexLexer):
    """Lexer for Xojo."""

    name = 'xojo'
    aliases = ['xojo']
    flags = re.IGNORECASE | re.UNICODE

    #pylint: disable=bad-continuation


    BUILTINS = ('AddHandler', 'Call', 'CurrentMethodName',
    'Raise', 'RemoveHandler')
    KEYWORDS = ('Aggregates', 'As', 'Assigns', 'Attributes', 'Break', 'ByRef', 'ByVal',
    'Case', 'Catch', 'Class', 'Continue', 'Delegate', 'Do', 'DownTo', 'Each',
    'Enum', 'Else', 'ElseIf', 'End', 'Event', 'Exception', 'Exit', 'Extends', 'Finally',
    'For', 'Function', 'Global', 'Handles', 'If', 'Implements', 'In', 'Inherits', 'Interface',
    'Lib', 'Loop', 'Module', 'Next', 'New', 'Namespace', 'Optional', 'ParamArray', 'Private',
    'Protected', 'Public', 'Return', 'Select', 'Selector', 'Step', 'Structure',
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
            (words(('Using', 'module'), suffix=r'\b'), Keyword.Namespace, 'namespace_decl'),
            (words(('GOTO',), suffix=r'\b'), Keyword.Reserved, 'goto'),
            (r'as\b', Keyword.Reserved, 'as'),


            (words(('self', 'me', 'super'), suffix=r'\b'), Name.Builtin.Pseudo),
            (DECLARE, using(_DeclareLexer)),
            #function|sub declaration
            (words(BUILTINS, suffix=r'\b'), Name.Builtin),
            (words(KEYWORDS, suffix=r'\b'), Keyword.Reserved),

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

            (r'(<=?)|(>=?)|(<>)|[\=\+\-\*/\^\<\>]', Operator),
            (words(OPERATOR_WORDS, prefix=r'\b', suffix=r'\b'), Operator.Word),
            (r'[(),.:]', Punctuation),
            (r'[^\d\W]\w*:', Name.Label),
            (IDENTIFIER, Name.Variable),
            ],

        'namespace_decl': [
            include('ignorable_whitespace'),
            (r'[^\d\W]\w*(.[^\d\W]\w*)*', Name.Namespace, '#pop'),
            ],

        'goto': [
            include('ignorable_whitespace'),
            (IDENTIFIER, Name.Label, '#pop'),
            ],

        'as': [
            include('ignorable_whitespace'),
            (IDENTIFIER, Name.XojoType, '#pop'),
            ],
        }
