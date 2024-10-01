# Read Me

For more details, refer to the [Microsite](https://github.com/Scattolin-Marco_bcgprod/boilerplate_2024/index.htm)

In case microsite is not available, you can access documentation here `docs/source`

## Quick Start

- create virtual environment

    ```
    python -m venv .venv
    ```

- activate virtual environment

    ```
    .venv/bin/activate
    ```
  - if on Windows use this

      ```
      .\.venv\Scripts\activate
      ```

- upgrade poetry

    ```
    python -m pip install --upgrade pip poetry
    ```

- suppress creation of poetry virtual environment with:
    ```
    poetry config virtualenvs.create false
    ```

- install dependencies with:

    ```
    poetry install
    ```    


## Optional

- install optional dependencies with:

    ```
    poetry install --with airflow
    ```
  Example here for airflow, check `pyproject.toml` for available optional dependencies.


- Install pre-commit hooks with:

    ```
    pre-commit install --install-hooks
    ```    
