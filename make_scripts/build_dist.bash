#! /bin/bash

NAME="pygments-xojo"
PKG="pygments_xojo"
BUILD_VENV="python3.4.venv"
SDIST_VENV="python-sdist.venv"
WHEEL_VENV="python-wheel.venv"
PYTHON="bin/python"
PIP="bin/pip"

PKG_VERSION=$(grep '__version__' pygments_xojo/__init__.py | cut -d '=' -f2 | cut -d "'" -f2)

echo "Building source distribution."
"$BUILD_VENV/$PYTHON" setup.py sdist

echo "Testing source distribution installation."
rm -rf "$SDIST_VENV"
virtualenv "$SDIST_VENV"
"$SDIST_VENV/$PIP" install "dist/$NAME-$PKG_VERSION.tar.gz"
#check import and version.
if ! "$SDIST_VENV/$PYTHON" -c "import $PKG" ; then
    echo "Source distribution failed; unable to import pygments_xojo."
    exit 1
fi

echo "Building binary distribution."
"$BUILD_VENV/$PYTHON" setup.py bdist_wheel

echo "Testing binary distribution installation."
rm -rf "$WHEEL_VENV"
virtualenv "$WHEEL_VENV"
"$WHEEL_VENV/$PIP" install "dist/$PKG-$PKG_VERSION-py2.py3-none-any.whl" 
#check import and version.
if ! "$WHEEL_VENV/$PYTHON" -c "import $PKG" ; then
    echo "Binary distribution failed; unable to import pygments_xojo."
    exit 1
fi