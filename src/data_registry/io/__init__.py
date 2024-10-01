import pandas as pd

from src.config.config import conf


class S3ParquetTable:

    path = None
    bucket_name = conf.s3_creds.bucket_name
    storage_options = {
        "key": conf.s3_creds.access_key,
        "secret": conf.s3_creds.secret_key.get_secret_value(),
    }


class S3PandasParquetTable(S3ParquetTable):
    @classmethod
    def read(cls, *args, **kwargs) -> pd.DataFrame:
        full_path = f"s3a://{cls.bucket_name}/{cls.path}"
        df = pd.read_parquet(
            full_path, storage_options=cls.storage_options, *args, **kwargs
        )
        return df

    @classmethod
    def write(cls, df: pd.DataFrame, *args, **kwargs) -> None:
        full_path = f"s3a://{cls.bucket_name}/{cls.path}"
        df.to_parquet(full_path, storage_options=cls.storage_options, *args, **kwargs)


class S3SparkParquetTable(S3ParquetTable):

    from src.utils.spark import spark

    @classmethod
    def read(cls):

        full_path = f"s3a://{cls.bucket_name}/{cls.path}"

        df = cls.spark.read.parquet(full_path)

        return df

    @classmethod
    def write(cls, df, *args, **kwargs):
        full_path = f"s3a://{cls.bucket_name}/{cls.path}"
        df = df.write.parquet(full_path, *args, **kwargs)
        return df
