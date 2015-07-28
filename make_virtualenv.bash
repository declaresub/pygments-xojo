#! /bin/bash


# Creates virtual environments for development using the Python executables in $ENV_LIST. 
# Existing environments are recreated.


PIP="pip"
VIRTUALENV="virtualenv"
ENV_LIST="python2 python3"
ENV_EXT="venv"

#let's make sure that pip and virtualenv are installed.
if ! hash "$PIP" 2>/dev/null; then
    echo "The ${PIP} command was not found." >&2
    exit 1
fi

if ! hash "$VIRTUALENV" 2>/dev/null; then
    echo "The ${VIRTUALENV} command was not found." >&2
    exit 1
fi

for ENV in $ENV_LIST;
    do
    if hash "$ENV" 2> /dev/null; then
        ENV_DIR="$ENV.$ENV_EXT"
        echo "Creating directory $ENV_DIR"
        rm -rf "$ENV_DIR"
        mkdir "$ENV_DIR"
        echo "Initializing virtualenv."
        virtualenv --python="$ENV" "$ENV_DIR"
        source "$ENV_DIR/bin/activate"
        echo "Installing this package."
        pip install --process-dependency-links  --editable .
        echo "Installing additional packages from requirements.txt."
        pip install -r requirements.txt
        deactivate
    fi  
    done