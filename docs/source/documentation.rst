Documentation
===========================================================================

The documentation is build using sphinx. Make sure you have installed
the :code:`docs` extra to get the required packages.

The documentation will be built by GitHub actions on every pull-request you make
to the repo and deployed on the main branch (e.g. when you merge a PR).

How to generate this documentation
############################################

Assuming all document files are in :code:`docs/source`

* Build source files with

.. code-block:: bash

    sphinx-build -a -b html docs/source docs/build/html

* Make sure an empty file :code:`.nojekyll` is also created into :code:`docs/build/html`, if not add it manually

* Publish docs with

.. code-block:: bash

    gh-pages --dotfiles --dist "docs/build/html"


Install gh-pages and publish
############################

* Install npm (if you're on MacOS use brew install npm)

.. code-block:: bash

    npm install -g gh-pages

on Mac M1 run

.. code-block:: bash

    npm install -D gh-pages@2.0

* On the GIT web interface ensure GH Pages is enabled for your repo and pick the right branch for it: Settings > Options > GitHub Pages > Source = 'gh-pages -> root'