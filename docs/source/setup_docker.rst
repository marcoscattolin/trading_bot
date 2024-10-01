Setup of dev environment via Docker
================================================

.. _dev docker setup:

This boilerplate is designed to be used alternatively with virtual environment or with docker containers.

In case of development of simple applications not requiring spark or airflow, it is recommended to use virtual environments, setup instructions available :ref:`here <dev venv setup>`

The following steps will guide you through the setup of a docker environment.


.. warning::
    When using docker setup it is nevertheless recommended to create a mirrored virtual environment. Pycharm in fact is not be able to recognize the dockerized interpreter and will not be able to provide code completion and other features.


Dockerized Development Environment
----------------------------------

This repository includes a dockerized virtual environment to simplify the execution of complex applications.

Following services are included in the docker-compose file:

    - :code:`pg_db`: container with a postgres database
    - :code:`basic_vm`: container with basic python packages (pandas, numpy, scikit-learn, etc.)
    - :code:`airflow_vm`: container with airflow
    - :code:`spark_vm`: container with spark

To build the image go to path :code:`./docker` and run

.. code-block:: bash

    docker-compose up <service_name>

Then in pycharm, add a new remote interpreter using the selected docker-compose service :code:`<service_name>` as remote interpreter. Here below the detailed steps:

    - In Pycharm, add new interpreter "On Docker Compose"
    - Select file `docker-compose.yml` and then service :code:`<service_name>`
    - Keep default python interpreter `/usr/bin/python3`

Now you can run python scripts from pycharm using the dockerized interpreter. Also debugging is available and happens directly on the docker container.


Service pg_db
----------------------------------

.. _database:

When this container is started, it will create a new database accessible using credentials defined in the environment file :code:`docker/.env`.

Default server name of database is :code:`pg_db`. Server name can be changed in :code:`docker/docker-compose.yml`.

Code can then access the database via credentials defined in the configuration file :code:`configs/credentials.yaml`. Note that this file will be available only after initialization of config files (see :ref:`config_files <config_files>`).




Service basic_vm
----------------------------------

.. _basic_vm:

When this container is started, it will create a new container with basic packages installed.

If needed, you can access the container shell and launch a jupyter notebook instance using the following command:

.. code-block:: bash

    jupyter notebook



Service airflow_vm
----------------------------------

.. _airflow_vm:

When this container is started, it will create a new airflow environment accessible at :code:`http://localhost:8080`.

Login credentials can be defined in the environment file :code:`docker/.env`.

DAGs can be added to the repository into :code:`dags` folder and will be automatically loaded into the airflow environment.

Jupyter notebook can be launched as described in the :ref:`basic_vm <basic_vm>` section.


Service spark_vm
----------------------------------

.. _spark_vm:

When this container is started, it will create a new container with spark available.

Code can import spark session defined in :code:`src/utils/spark.py` as follows:

.. code-block:: python

    from src.utils.spark import spark

    spark = spark.read.parquet("<file_path>")


Spark UI is accessible at :code:`http://localhost:4040` while spark jobs are running.

Jupyter notebook can be launched as described in the :ref:`basic_vm <basic_vm>` section.

By default spark session is created with support for S3 I/O operations. S3 credentials can be defined in the configuration file :code:`configs/credentials.yaml`. Note that this file will be available only after initialization of config files (see :ref:`config_files <config_files>`).
