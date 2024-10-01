Repository Structure
=====================

.. _repo_structure:


Configuration
------------------------

.. _config_files:

The repository uses a Pydantic-based approach facilitated by XConfig, a library developed by BCG
internally. When cloning your first instance of the repo, you will get a lot of defaults values
already attached to the Pydantic models. Default configurations are stored in :code:`src/config/templates`. Some values are not set (especially secrets).

To create config files from templates, you can run

.. code-block:: bash

    python -m src init

This copies the default configuration files into :code:`configs` folder and you can start editing parameters as you like.

If you need to extend the configuration, you need to

    - edit the templates in :code:`src/config/templates` editing existing yaml files or adding new ones
    - edit the Pydantic models in :code:`src/config/config.py` accordingly
    - edit the XConfig class in :code:`src/config/xconfig.py` accordingly
    - reinitialize the configuration files with :code:`python -m src init` or alternatively editing/adding the yaml files in the :code:`configs` folder


Logging
-------------------

The repository provides a centralized logger that can be used as follows:

.. code-block:: python

    from src.utils.logging import logger

    logger.info("Hello world")

Logs are saved into the :code:`logs` folder. Log files are saved with a rotating logic by which max 5 log files are kept and each log file is max 10MB.


Jupyter Notebook
----------------------------

The repository provides a Jupyter Notebook server. Depending on your setup (virtual env or docker), you can start the server as follows:

If using a virtual environment:

    - activate the virtual environment
    - run the following command


.. code-block:: bash

    jupyter notebook

If using Docker:

    - start the docker container (ie. one of the containers provided in the :code:`docker/docker_compose.yml`)
    - access the container terminal
    - run the following command


.. code-block:: bash

    jupyter notebook


Spark support via Docker
--------------------------

If using spark_vm docker container, the repository provides a centralized spark session that can be used in the code.

See :ref:`spark_vm <spark_vm>` for details.


Database support via Docker
---------------------------

If needed, the user can start the pg_db service, which in turns provides a postgres database.

(see :ref:`database <database>` for details)


Airflow support via Docker
--------------------------

If using airflow_vm docker container, the repository provides an airflow webserver and scheduler that can be used to schedule and monitor tasks.

See :ref:`airflow_vm <airflow_vm>` for details.
