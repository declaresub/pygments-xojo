# -*- coding: utf-8 -*-
"""
Lexer for the Xojo language.

:copyright: Copyright 2015 Charles Yeomans.
:license: BSD, see LICENSE for details.
"""

from __future__ import absolute_import
import re
from pygments.lexer import RegexLexer, bygroups, words, include, default, using, this
from pygments.token import Keyword, Name, String, Literal, Number, Punctuation, Comment, \
    Operator, Text, Error


__all__ = ['XojoLexer']


# various regular expressions
IDENTIFIER = r'[^\d\W]\w*'
IDENTIFIER_FQ = r'[^\d\W]\w*(\.[^\d\W]\w*)*'
LITERAL_STRING = r'"(""|[^"])*"'
LITERAL_UNICODE = r'&u[0-9a-fA-F]+'
WHITESPACE = r'[\ \t]+'
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
    'Case', 'Catch', 'Class', 'Continue', 'Do', 'DownTo', 'Each',
    'Enum', 'Else', 'ElseIf', 'End', 'Event', 'Exception', 'Exit', 'Extends', 'Finally',
    'For', 'Function', 'Global', 'Handles', 'If', 'Implements', 'In', 'Inherits', 'Interface',
    'Lib', 'Loop', 'Module', 'Next', 'New', 'Namespace', 'Optional', 'ParamArray', 'Private',
    'Protected', 'Public', 'Return', 'Select', 'Selector', 'Shared', 'Soft', 'Step', 'Structure',
    'Sub', 'Then', 'To', 'Try', 'Until', 'Wend', 'While', 'With', 'WithEvents',
    '#if', '#else', '#elseif', '#endif', '#pragma']
    OPERATOR_WORDS = ['And', 'Is', 'IsA', 'Mod', 'Not', 'Or', 'Xor', 'AddressOf', 'Array',
    'Ctype', 'GetTypeInfo', 'RaiseEvent', 'Redim', 'WeakAddressOf']
    TYPES = ['Boolean', 'Byte', 'Color', 'Currency', 'Delegate', 'Double', 'Integer',
    'Int8', 'Int16', 'Int32', 'Int64', 'UInt8', 'UInt16', 'UInt32', 'UInt64', 'Short', 'Single', 'String',
    'Structure']
    tokens = {
        'whitespace': [
            (r'[\ \t]+', Text),
            ],

        'function_decl': [
            (words(['function', 'sub', 'event'], suffix=WORD_SUFFIX), Keyword.Reserved, 'function_name'),
                ],
                

        'root': [
            include('whitespace'),
            (words(['#tag'], suffix=WORD_SUFFIX), Comment.Preproc),
            (words(DECLARATIONS, suffix=WORD_SUFFIX), Keyword.Declaration),
            (words(CONSTANTS, suffix=WORD_SUFFIX), Keyword.Constant),
            (words(PSEUDO_BUILTINS, suffix=WORD_SUFFIX), Name.Builtin.Pseudo),
            (words(('Using', 'module'), suffix=WORD_SUFFIX), Keyword.Namespace, 'namespace_name'),
            (words(['class'], suffix=WORD_SUFFIX), Keyword.Reserved, 'class_name'),
            include('function_decl'),
            (words(['property'], suffix=WORD_SUFFIX), Keyword.Reserved, 'property_decl'), 
            (words(['as'], suffix=WORD_SUFFIX), Keyword.Reserved, 'as'),
            (words(['declare'], suffix=WORD_SUFFIX), Keyword.Declaration, 'declare'),
            (words(['GOTO'], suffix=WORD_SUFFIX), Keyword.Reserved, 'goto'),
            (words(BUILTINS, suffix=WORD_SUFFIX), Name.Builtin),
            (words(KEYWORDS, suffix=WORD_SUFFIX), Keyword.Reserved),
            (words(TYPES, suffix=WORD_SUFFIX), Keyword.Type),
                 
            # Literals
            (LITERAL_STRING, String),
            (LITERAL_UNICODE, Literal.Unicode),
            (r'([0-9]*\.[0-9]+)([eE][-+]?[0-9]+)?', bygroups(Number.Float, Number.Float)),
            (r'[0-9]+', Number.Integer),
                 
            (r'(&b[01]+)(\s+)', bygroups(Number.Bin, Text)),
            (r'(&b[01]+)(_|,|[)])', bygroups(Number.Bin, Punctuation)),
            (r'(&b[01]+)(\'|//)', bygroups(Number.Bin, Comment),'comment_url'),
            (r'(&b[01]+)(<>|<=?|>=?|[-=+*/^\\])', bygroups(Number.Bin, Operator)),
                 
            (r'(&o[0-7]+)(\s+)', bygroups(Number.Oct, Text)),
            (r'(&o[0-7]+)(_|,|[)])', bygroups(Number.Oct, Punctuation)),
            (r'(&o[0-7]+)(\'|//)', bygroups(Number.Oct, Comment),'comment_url'),
            (r'(&o[0-7]+)(<>|<=?|>=?|[-=+*/^\\])', bygroups(Number.Oct, Operator)),
                 
            (r'(&h[0-9a-fA-F]+)(\s+)', bygroups(Number.Oct, Text)),
            (r'(&h[0-9a-fA-F]+)(_|,|[)])', bygroups(Number.Oct, Punctuation)),
            (r'(&h[0-9a-fA-F]+)(\'|//)', bygroups(Number.Hex, Comment),'comment_url'),
            (r'(&h[0-9a-fA-F]+)(<>|<=?|>=?|[-=+*/^\\])', bygroups(Number.Hex, Operator)),
           
            (r'(&c)([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})?',
             bygroups(Name.XojoType.Color, Name.XojoType.Color.Red, Name.XojoType.Color.Green,
                      Name.XojoType.Color.Blue, Name.XojoType.Color.Alpha)),

            # line continuation
            (r'_(?!\w)', Punctuation),
            (r'\'', Comment, 'comment_url'),
            (r'//', Comment, 'comment_url'),
            (r'REM\b', Comment, 'comment_url'),

            (r'<>|<=?|>=?|[-=+*/^\\]', Operator),
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
            
        'property_decl': [
            # this is a distinct state because get, set are keywords only within a structure
            # declaration.
            (words(['get', 'set']), Keyword.Reserved),
            # RegexLexer resets the state stack to ['root'] when it encounters \n.  By 
            # consuming the linefeed, we prevent this and keep the stack state as we want.
            ('\n', Text),
            include('root'),
            (r'end property', Keyword.Reserved, '#pop'),
            ],

        'comment_url': [
            (r'http\://\S*', Comment.URL),
            (r'https\://\S*', Comment.URL),
            (r'ftp\://\S*', Comment.URL),
            (r'ftps\://\S*', Comment.URL),
            (r'rb-feedback\://\S*', Comment.URL),
            (r'feedback\://\S*', Comment.URL),
            (r'mailto\:\S*', Comment.URL),
            ('\n', Comment, '#pop'),
            (r'.', Comment),
            ],

        }
