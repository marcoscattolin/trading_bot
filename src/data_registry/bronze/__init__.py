from src.data_registry.io import S3SparkParquetTable as Table


class DummyTable(Table):

    column1 = "int_col"
    column2 = "float_col"
    column3 = "bool_col"
    column4 = "string_col"
    column5 = "time_col"
    column6 = "date_col"

    path = "path/to/dummy_test.parquet"


if __name__ == "__main__":

    tab = DummyTable.read()

    print(tab.show())
    print(tab.dtypes)

    DummyTable.write(df=tab, mode="overwrite")
    print("Done")
