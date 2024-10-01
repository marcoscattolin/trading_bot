Setup of dev environment via Virtual Environment
================================================

.. _dev venv setup:

This boilerplate is designed to be used alternatively with virtual environment or with docker containers.

In case of development of complex applications requiring spark or airflow, it is recommended to use docker containers, setup instructions available :ref:`here <dev docker setup>`

The following steps will guide you through the setup of a virtual environment.


Create Virtual Environment
--------------------------

In github, create a new repository selecting this repo as a template. Clone the repo in pycharm and mark directory :code:`src` as sources Root.

Make sure python executable refers to the python version defined in :code:`pyproject.toml`

Create a new virtual environment with command:

.. code-block:: bash

    python -m venv .venv

and activate it with command:

.. code-block:: bash

    .venv\Scripts\activate


Packages installation
---------------------------------------------

To install requirements and packages use :code:`poetry`. Following commands will install default dependencies
and pre-commit hooks.

.. code-block:: bash

    python -m pip install --upgrade pip poetry

Suppress creation of poetry virtual environment with:

.. code-block:: bash

    poetry config virtualenvs.create false

Install dependencies with:

.. code-block:: bash

    poetry install


[Optional] Packages installation
---------------------------------------------

Alternatively, you can install optional dependencies. For example, if you need airflow:

.. code-block:: bash

    poetry install --with airflow

Check the :code:`pyproject.toml` file for the list of available extras.

Pre-commit hooks installation
---------------------------------------------


Next, install the pre-commit hooks using

.. code-block:: bash

    pre-commit install --install-hooks

You can verify the installation by running the test suite.

Setup pycharm interpreter
-------------------------

In Pycharm set the newly created virtual environment as the project interpreter. In order to do so

    - click on bottom right corner of the window on the interpreter name
    - select :code:`Add new interpreter`
    - select :code:`Add local interpreter`
    - select :code:`Virtualenv environment`
    - select :code:`Existing environment`
    - make sure the path refers to :code:`<repo>\.venv\Scripts\python.exe`
