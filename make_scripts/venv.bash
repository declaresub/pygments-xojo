#! /bin/bash


# Creates virtual environments for development using the Python executables in $ENV_LIST. 
# Existing environments are recreated.


PIP="pip"
VIRTUALENV="virtualenv"
PYVENV="pyvenv"
PYVERSIONS="2.6 2.7 3.3 3.4"
ENV_EXT="venv"


for VERSION in $PYVERSIONS;
    do
    #first, look for pyvenv; it should be available for $VERSION >= '3.3.
    
    
    VENV="$PYVENV-$VERSION"
    if ! hash "$VENV" 2> /dev/null; then
        #not found, so fall back to virtualenv.
        VENV="$VIRTUALENV"
        VENV_ARGS="--python=python$VERSION --clear "
    else
        VENV_ARGS="--clear"
    fi
    if hash "$VENV" 2> /dev/null; then
        ENV_DIR="python$VERSION.$ENV_EXT"
        #echo "Creating directory $ENV_DIR"
        #rm -rf "$ENV_DIR"
        #mkdir "$ENV_DIR"
        echo "Initializing virtualenv."
        "$VENV" $VENV_ARGS "$ENV_DIR"
        source "$ENV_DIR/bin/activate"
        
        #check for pip install in this virtual environment.
        if [[ ! -x $VIRTUAL_ENV/bin/pip ]]; then
            echo "pip is not included in this virtual environment. Installing pip."
            if [[ ! =f get-pip.py ]]; then
                curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
            fi
            python get-pip.py   
        fi
        
        echo "Installing this package."
        pip install --process-dependency-links  --editable .
        echo "Installing additional packages from requirements.txt."
        pip install -r requirements.txt
        deactivate
    fi  
    done
    rm -f get-pip.py
