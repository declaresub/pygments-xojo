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
from pygments.lexer import RegexLexer, words, include, default
from pygments.token import Keyword, Name, String, Literal, Number, Punctuation, Comment, \
    Operator, Text

__all__ = ['XojoLexer']


# various regular expressions
IDENTIFIER = r'[^\d\W]\w*'




class _DeclareSubLexer(RegexLexer):
    pass
               
                            
class _DeclareFunctionLexer(RegexLexer):
    pass
    
class _FunctionParamsLexer(RegexLexer):
    name = 'xojofunctionparam'
    aliases = ['xojofunctionparam']
    flags = re.IGNORECASE | re.UNICODE     
    
    tokens = {
        'ignorable_whitespace': [
            (r'[\ \t]+', Text),
            ],
            
        'root': [
            include('ignorable_whitespace'),
            (IDENTIFIER, Name.Variable, 'param_as'), 
            ],        
    
        'param_as': [
            include('ignorable_whitespace'),
            (r'as', Keyword.Reserved, 'param_type')
            ],
            
        'param_type': [
            include('ignorable_whitespace'),
            (IDENTIFIER, Name, 'param_sep'), 
            ],

        'param_sep': [
            include('ignorable_whitespace'),
            (r'\,', Punctuation, 'root'),
            default('#pop'),
            ],
        }

class XojoLexer(RegexLexer):
    """Lexer for Xojo."""

    name = 'xojo'
    aliases = ['xojo']
    flags = re.IGNORECASE | re.UNICODE

    #pylint: disable=bad-continuation
    IDENTIFIER = r'[^\d\W]\w*'
    IDENTIFIER_FQ = r'[^\d\W]\w*(\.[^\d\W]\w*)*'
    LITERAL_STRING = r'"(""|[^"])*"'
    LITERAL_UNICODE = r'&u[0-9a-fA-F]+'
    
    BUILTINS = ('AddHandler', 'Call','CurrentMethodName',
    'Raise',  'RemoveHandler')
    KEYWORDS = ('Aggregates', 'As', 'Assigns', 'Attributes', 'Break', 'ByRef', 'ByVal',
    'Case', 'Catch', 'Class', 'Continue', 'Declare', 'Delegate', 'Do', 'DownTo', 'Each',
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
            (words(BUILTINS, suffix=r'\b'), Name.Builtin),
            (words(('Using', 'module'), suffix=r'\b'), Keyword.Namespace, 'namespace_decl'),
            (words(('GOTO',), suffix=r'\b'), Keyword.Reserved, 'goto'),
            (words(('self', 'me', 'super'), suffix=r'\b'), Name.Builtin.Pseudo),
            (words(KEYWORDS, suffix=r'\b'), Keyword.Reserved),

            # Literals
            (LITERAL_STRING, String),
            (LITERAL_UNICODE, Literal),
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



        'namespace_decl': [
            include('ignorable_whitespace'),
            (r'[^\d\W]\w*(.[^\d\W]\w*)*', Name.Namespace, '#pop'),
            ],

        'goto': [
            include('ignorable_whitespace'),
            (IDENTIFIER, Name.Label, '#pop'),
            ],

       
         
         #use multiple lexers to read declare sub v. function statements.  


            

            
        }
        

