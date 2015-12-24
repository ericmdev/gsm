gsm (Git Submodule Manager)
===========================

Easily manage git submodules using a `gitsubmodule.json`.

Requirements
------------

Requires `Python 2.7`.

To check your version of Python:

    $ python --version
    # Python 2.7.10

Usage
-----

Enter your git submodule dependencies in `gitsubmodule.json` using the format `destination:source`, e.g:

    {
      "dependencies": {
        "bin/lib/gist_example": "https://gist.github.com/my_gist.git"
      }, 
      "devDependencies": {}
    }

*HTTPS is recommended by Github and preferred to SSH.

The above `gitsubmodule.json` tells gsm to clone the gist into our project (as a git submodule) in the directory `bin/lib/gist_example`.

All we have to do now is run gsm:

    $ python gsm.py



