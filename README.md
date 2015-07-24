# Pygments-Xojo

Pygments-Xojo implements Xojo language markup for [Pygments](http://pygments.org/), the 
Python syntax highlighter.

To try it out, clone this repository to your computer.  Pygments requires Python >= 2.6 or >= 3.3,
so you'll need the same, plus pip and virtualenv.  The project is set up to use tox for testing, 
but as of now there is only one smoke test, so you can skip this.

Once your Python world is configured, run the script make_virtualenv.bash.  This will create
virtual environments for Python2 and Python3, if installed.  To activate a virtual 
environment, open a Terminal window and cd to the repository directory.  Then execute the 
following command (assuming you want to use Python 2).

    source python2.env/bin/activate
    
You can format some Xojo code in a file /path/to/foo as follows.

    pygmentize -f html  -l xojo /path/to/foo
    
which writes output to stdout, or

    pygmentize -f html  -l xojo /path/to/foo /path/to/foo.html
    
which writes the output to a file that you can view in the browser of your choice.
