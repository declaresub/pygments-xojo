from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys
import string
import io


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
    license='BSD',
    packages=['pygments_xojo'],
    install_requires=['pygments'],
    entry_points = {'pygments.lexers': ['xojo = pygments_xojo.xojo:XojoLexer'], 'pygments.styles': ['xojo = pygments_xojo.xojostyle:XojoStyle']},
    cmdclass = {'test': Tox}
    )
