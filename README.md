# Pygments-Xojo

Pygments-Xojo implements Xojo language markup for [Pygments](http://pygments.org/), the 
Python syntax highlighter.

Like Pygments, Pygments-Xojo requires Python >= 2.6 or >= 3.3.

To try it out, clone this repository to your computer.  If you don't have a supported 
version of Python installed, you can [download](https://www.python.org/downloads/) an 
installer or build from source, depending on your platform and preferences.  If you are 
working on a Mac, you'll save a lot of annoyance by installing a version of Python for 
your own work instead of using the system install.

You will need pip, a Python package manager.  This is included with Python 3.4; if you 
want to use an earlier version, you'll need to install it yourself.  

    curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
    sudo python get-pip.py   

And if you are using Python 2, you will also need to install virtualenv.

    sudo pip install virtualenv

Once your Python world is configured, run `make venv`.  This will create
virtual environments for all supported Python versions installed on your machine.  These 
are installed mostly for testing.  You can activate the one for your preferred Python version.
You can delete the other .venv directories to reduce perceived clutter, or run `make clean` 
to get rid of all of them.

To activate a virtual environment, open a Terminal window and cd to the repository directory.  
Then execute the following command (assuming you want to use Python 3.4).

    source python3.4.env/bin/activate
    
You can now format some Xojo code in a file /path/to/foo as follows.

    pygmentize -O full,style=xojo,linenos=1 -f html -l xojo /path/to/foo
    
which writes output to stdout, or

    pygmentize -O full,style=xojo,linenos=1 -f html -l xojo -o /path/to/foo.html /path/to/foo 
    
which writes the output to a file that you can view in the browser of your choice.


![Travis Build Status](https://travis-ci.org/declaresub/pygments-xojo.svg?branch=master)