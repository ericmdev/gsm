gsm (Git Submodule Manager)
===========================

Easily manage git submodules using a `gitsubmodule.json` file.

Requirements
------------

Requires:

- `Git 2.4`
- `Python 2.7`

To check your version of Git:

    $ git --version
    # git version 2.4.9 (Apple Git-60)

To check your version of Python:

    $ python --version
    # Python 2.7.10

Usage
-----

Acquire gsm.py:

    $ wget https://raw.githubusercontent.com/ericmdev/gsm/master/gsm.py -O gsm.py


Enter your git submodule dependencies in `gitsubmodule.json` using the format `path:source`, e.g:

    {
      "dependencies": {
        "bin/lib/gist_example": "https://gist.github.com/my_gist.git"
      }, 
      "devDependencies": {}
    }

*HTTPS is recommended by Github and preferred to SSH.

The above `gitsubmodule.json` tells gsm to clone the gist into our project as a git submodule in the directory `bin/lib/gist_example`.

All we have to do now is run gsm:

    $ python gsm.py

This will execute the following command for all dependencies listed in `gitsubmodule.json`:

    $ git submodule add [[source]] [[path]]

