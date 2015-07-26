# -*- coding: utf-8 -*-


"""Pygments syntax highlighting for Xojo."""


from pygments.token import Token
# the point of the next statement is that accessing the attribute creates the token type,
# as explained in the pygments token documentation.
#pylint:disable=pointless-statement
Token.Name.XojoType

# __version is also read by setup.py.
__version__ = '0.0.0'
