gsm (Git Submodule Manager)
===========================

Easily manage git submodules using a `gitsubmodule.json` file.

Requirements
------------

Requires `PHP 5.6+`.

To check your version of PHP:

    $ php -v
    # PHP 5.6.16 (cli) (built: Nov 27 2015 10:28:34)
    # Copyright (c) 1997-2015 The PHP Group
    # Zend Engine v2.6.0, Copyright (c) 1998-2015 Zend Technologies
    #     with Zend OPcache v7.0.6-dev, Copyright (c) 1999-2015, by Zend Technologies

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

The above `gitsubmodule.json` tells gsm to clone the gist into our project as a git submodule in the directory `bin/lib/gist_example`.

All we have to do now is run gsm:

    $ php gsm.phar



