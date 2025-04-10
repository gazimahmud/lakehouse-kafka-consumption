from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

message = {
    "instruction": "load data to delta table",
    "source_path": "s3a://bucket_name/cts_output/sample.csv",
    "delta_path": "s3a://bucket_name/cts_payload/delta/events",
    "namespace": "CTS_Payload",
    "table_name": "cts_job_results",
    "job_id": "job_001"
}

producer.send("csv-files", message)
producer.flush()
print("Message sent to Kafka!")
