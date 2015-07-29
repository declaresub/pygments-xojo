# -*- coding: utf-8 -*-

"""Pygments-Xojo
   ^^^^^^^^^^^^^

Pygments-Xojo adds support for the Xojo language to the Pygments syntax highlighting
package.

    :copyright: Copyright 2015 Charles Yeomans.
    :license: BSD, see LICENSE for details.
"""

from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import string


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)

def package_version():
    with io.open('pygments_xojo/__init__.py', 'r', encoding='utf-8') as f:
        for sourceline in f:
            if sourceline.strip().startswith('__version__'):
                 return sourceline.split('=', 1)[1].strip(string.whitespace + '"\'')
        else:
            raise Exception('Unable to read package version.')

setup(name='pygments-xojo',
    version=package_version(),
    author='Charles Yeomans', 
    author_email='charles@declaresub.com',
    license='BSD License',
    url='https://github.com/declaresub/pygments-xojo',
    description='Pygments highlighting for the Xojo language',
    long_description = __doc__,
    keywords = 'syntax highlighting xojo',
    platforms = 'any',
    packages=['pygments_xojo'],
    install_requires=['pygments'],
    entry_points = {'pygments.lexers': ['xojo = pygments_xojo.lexer:XojoLexer'], 'pygments.styles': ['xojo = pygments_xojo.styles:XojoStyle']},
    cmdclass = {'test': Tox}
    )
