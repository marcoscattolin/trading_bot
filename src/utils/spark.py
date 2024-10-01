#  Copyright (c) 2023, Boston Consulting Group.
#  Authors: Marco Scattolin
#  License: Proprietary

from pyspark.sql import SparkSession, SQLContext

from src.config import conf


def spark_init():

    # s3 credentials
    access_key = conf.s3_creds.access_key
    secret_key = conf.s3_creds.secret_key.get_secret_value()

    # spark configuration
    master = conf.spark_connection.master
    driver_memory = conf.spark_connection.driver_memory
    network_timeout = conf.spark_connection.network_timeout

    _spark = (
        SparkSession.builder.appName("Spark Example")
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )
        .config("spark.hadoop.fs.s3a.access.key", access_key)
        .config("spark.hadoop.fs.s3a.secret.key", secret_key)
        .config("spark.driver.memory", driver_memory)
        .config(
            "spark.jars",
            "/opt/spark/jars/aws-java-sdk-bundle-1.12.594.jar,"
            "/opt/spark/jars/hadoop-aws-3.3.4.jar,"
            "/opt/spark/jars/postgresql-42.5.4.jar,"
            "/opt/spark/jars/hadoop-common-3.3.4.jar",
        )
        .config("spark.network.timeout", network_timeout)
        .master(master)
        .getOrCreate()
    )
    _spark.sparkContext.setLogLevel("ERROR")

    sc = _spark.sparkContext
    _sqlContext = SQLContext(sc)

    return _spark, _sqlContext


(spark, sqlContext) = spark_init()
spark.sparkContext.setLogLevel("ERROR")
