# META-Aqua-Lene [![Build Status][travis_img]][travis_url] #
**A frame extraction tool for META-Aqua**

META-Aqua is a reasoner about the reasoning tool Aqua and performs Meta
reasoning to explain errors or anomalies in artificial cognition. META-Aqua
performs its task in a Top-Down fashion and includes a large knowledge
base stored as frames with slots.

This Python tool is designed to extract those frames from the Lisp KB and
present them as a Python object that can then be used to convert the frame
representation into another, suitable for other applications. For example
this tool can convert the frames into an RDF-format.

## Installation ##

You can install lene by using the setup.py script included with this
package:

    python setup.py install

This will also include all the requirements as found in the
requirements.txt file in this package. I have also included a Makefile for
ease of use also, and you can install the package with:

    make install
    make clean

For development you may want to create a virtual environment and install
the requirements without installing the lene package. If you already have
[virtualenv][virtualenv] installed, then simply create an environment and
then install the required packages:

    virtualenv venv
    pip install -r requirements.txt

It is highly recommended that you also use [virtualenvwrapper][virtualenvwrapper],
which provides extremely flexible environment management. Please do not
commit any environment files or packages.

## Usage ##

To interpret a Lisp file with `lene`, you can use the `load` or `loads`
functions to parse a .lisp file into a Python object- a list based Tree.

    data = lene.load(open('rep_fire.lisp'))

This structure can then be read for linkages to convert to an RDF document.

### Testing ###
This package is unit tested with `nosetests`. In the root of the package
you can simply run `nosetests -v` and the test discovery runner will
automatically locate the tests and execute them. Please also ensure that
the directory you're in can import the `lene` package.

Alternatively, you can run all the tests with coverage using:

    make test

Which will also report how much of the package is being tested.

This package is also tested with Travis-CI, meaning that on every commit,
the test suite is run in a virtual environment in Travis. If the tests
fail, then they are reported back to us via email. Please ensure that you
have run `make test` and successfully passed those tests before commiting
to the Master branch.

## TODO ##

* Base libraries
* Test framework
* RDF extractor
* Query explanation

## About ##
The Norwegian dance-pop group [Aqua][aqua_official] is best
known for their 1997 breakout single, [Barbie Girl][barbie_girl]. Although
META-Aqua is not named for this group, they do share a homonym. Their lead
singer is [Lene Nystrøm][nystrøm] and it is after her that this package is
named. (e.g. META-Aqua → Aqua → Lene)

<!-- References -->
[travis_img]: https://travis-ci.org/mclumd/lene.png?branch=master
[travis_url]: https://travis-ci.org/mclumd/lene
[aqua_official]: http://www.aquaofficial.com/
[barbie_girl]: http://www.youtube.com/watch?v=ZyhrYis509A‎
[nystrøm]: http://en.wikipedia.org/wiki/Lene_Nystr%C3%B8m
[virtualenv]: http://www.virtualenv.org/en/latest/virtualenv.html
[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org/en/latest/
