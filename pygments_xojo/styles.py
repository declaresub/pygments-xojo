# -*- coding: utf-8 -*-
"""
Style for the Xojo language.
"""


from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Literal

__all__ = ['XojoStyle']

#pylint: disable=too-few-public-methods
class XojoStyle(Style):
    """The default Xojo IDE style."""

    default_style = ""
    styles = {
        # Whitespace: "#bbbbbb",
        Comment: "#921100",
        Comment.URL: "underline #0C33FE",
        Comment.Preproc: "#0C33FE",
        Keyword: "#0C33FE",

        Operator: "#000000",
        Operator.Word: "#0C33FE",

        Name: "#000000",
        Name.Builtin: "#0C33FE",
        Name.Function: "#0C33FE",
        # Name.Class: "#000000",
        # Name.Namespace: "#000000",
        # Name.Exception: "bold #D2413A",
        # Name.Variable: "#000000",
        # Name.Constant: "#880000",
        # Name.Label: "#000000",
        # Name.Entity: "bold #999999",
        # Name.Attribute: "#7D9029",
        # Name.Tag: "bold #008000",
        Name.Decorator: "#AA22FF",
        Name.XojoType: "#0C33FE",

        String: "#7A35FD",
        # String.Doc: "italic",
        # String.Interpol: "bold #BB6688",
        # String.Escape: "bold #BB6622",
        # String.Regex: "#BB6688",
        # String.Symbol: "#B8860B",
        # String.Symbol: "#19177C",
        # String.Other: "#008000",
        
        Number: "#417AA8",
        Number.Float: "#007642",
        
        Literal: "#417AA8",
        Literal.Unicode: "#7A35FD",
        Name.XojoType.Color: "#000000",
        Name.XojoType.Color.Red: "#BA1600",
        Name.XojoType.Color.Green: "#00AB0D",
        Name.XojoType.Color.Blue: "#0520AF",
        Name.XojoType.Color.Alpha: "#000000",

        # Generic.Heading: "bold #000080",
        # Generic.Subheading: "bold #800080",
        # Generic.Deleted: "#A00000",
        # Generic.Inserted: "#00A000",
        # Generic.Error: "#FF0000",
        # Generic.Emph: "italic",
        # Generic.Strong: "bold",
        # Generic.Prompt: "bold #000080",
        # Generic.Output: "#888",
        # Generic.Traceback: "#04D",

        Error: "border:#FF2500 bg:#E5E5E5"
        }
