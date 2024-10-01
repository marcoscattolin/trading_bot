#  Copyright (c) 2024, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator

from src.config import conf

with DAG(
    "dag_example",
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "max_active_runs": 1,
    },
    description="DAG example",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    @task()
    def task_python():
        from src.code_examples import examples

        examples.run()

    task_bash = BashOperator(
        task_id="task_bash",
        bash_command="echo 'Hello World!'",
    )

    task_telegram = TelegramOperator(
        task_id="send_message_telegram",
        telegram_conn_id="telegram_default",
        token=conf.telegram_creds.token.get_secret_value(),
        chat_id=conf.telegram_creds.chat_id,
        text="Hello world!",
    )

    # Define sequence of tasks
    [task_python() >> task_bash >> task_telegram]
