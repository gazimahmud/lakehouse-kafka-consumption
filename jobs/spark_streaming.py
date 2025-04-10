import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

# Read MinIO credentials from environment
minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")

# Updated schema for structured Kafka messages
schema = StructType() \
    .add("instruction", StringType()) \
    .add("source_path", StringType()) \
    .add("delta_path", StringType()) \
    .add("namespace", StringType()) \
    .add("table_name", StringType()) \
    .add("job_id", StringType())

spark = SparkSession.builder \
    .appName("CSV to Delta Lake Stream") \
    .config("spark.jars.packages", \
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1," +
            "io.delta:delta-core_2.12:2.4.0," +
            "org.apache.hadoop:hadoop-aws:3.3.4") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", minio_access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key) \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "csv-files") \
    .option("startingOffsets", "earliest") \
    .load()

parsed_df = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

def load_csv_to_delta(batch_df, batch_id):
    records = batch_df.collect()
    for record in records:
        if record["instruction"] == "load data to delta table":
            try:
                csv_df = spark.read.option("header", True).csv(record["source_path"])
                csv_df.write.format("delta").mode("append").save(record["delta_path"])
                print(f"Successfully processed job {record['job_id']}.")
            except Exception as e:
                print(f"Error processing job {record['job_id']}: {e}")

query = parsed_df.writeStream \
    .foreachBatch(load_csv_to_delta) \
    .start()

query.awaitTermination()