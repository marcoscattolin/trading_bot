#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary


import pandas as pd

from src.utils.logging import logger


def load_data():

    df = pd.DataFrame(
        {
            "int_col": [1, 2, 3],
            "float_col": [1.1, 2.2, 3.3],
            "bool_col": [True, False, True],
            "string_col": ["pippo", "pluto", "paperino"],
            "time_col": pd.date_range(start="2024-01-01", periods=3, freq="12H"),
        }
    )
    df["date_col"] = pd.to_datetime(df["time_col"]).dt.date

    return df


def run():

    logger.info("+++++ CODE EXAMPLE +++++")

    df = load_data()

    logger.info("Dataframe head:")
    logger.info(df.head())

    logger.info("----- CODE EXAMPLE -----")


if __name__ == "__main__":
    run()
