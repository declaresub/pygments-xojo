#! /bin/bash


#do this inside my dev venv
python2.7.venv/bin/python setup.py sdist
python2.7.venv.venv/bin/python setup.py bdist_wheel
rm -rf python2.7-sdist.venv

virtualenv python2.7-sdist.venv
python2.7-sdist.venv/bin/pip install dist/pygments-xojo-0.0.0.tar.gz
#check import and version.
#python2.7-sdist.venv/bin/python -c 'from pygments_xojo import __version__;print(__version__)'