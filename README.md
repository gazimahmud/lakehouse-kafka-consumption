## This is a scaffolded multi-component Kubernetes-based Data Lakehouse prototype project
version: '0.1'
components:
  - name: documentation
    files:
      - README.md
        content: |
          # Lakehouse Prototype on Kubernetes (Local Workstation / MacBook)

          This project demonstrates a modern, end-to-end **Lakehouse architecture** running entirely on your local machine using containers and Kubernetes. It includes:

          - **MinIO** as an S3-compatible object storage layer
          - **Apache Kafka (KRaft mode)** for streaming ingestion (no Zookeeper)
          - **Apache Spark + Delta Lake** for data processing
          - **JupyterHub** for interactive exploration
          - **Kubernetes via KIND** to orchestrate everything locally

          This setup is ideal for development, experimentation, and education.

          ---

          ## Prerequisites

          Ensure the following tools are installed:

          | Tool          | Purpose                        | Install Link |
          |---------------|--------------------------------|--------------|
          | Docker        | Container runtime              | https://www.docker.com/products/docker-desktop/ |
          | KIND          | Local Kubernetes cluster       | https://kind.sigs.k8s.io/ |
          | kubectl       | Kubernetes CLI                 | https://kubernetes.io/docs/tasks/tools/ |
          | Python ≥3.9   | Scripting & Kafka producer     | https://www.python.org/downloads/ |
          | make (optional)| Task automation tool          | Built-in (Mac/Linux) or via Homebrew |

          ---

          ## Project Structure

          ```text
          ├── kind-config.yaml               # KIND cluster definition
          ├── manifests/                     # Kubernetes YAML manifests
          │   ├── kafka/                     # Kafka deployment (KRaft mode)
          │   ├── minio/                     # MinIO object store
          │   ├── spark/                     # Spark master/worker/job
          │   └── jupyterhub/                # JupyterHub environment
          ├── jobs/spark_streaming.py        # Spark structured streaming app
          ├── scripts/send_kafka_message.py  # Kafka producer script
          ├── Makefile                       # Local automation commands
          ├── .gitignore
          └── README.md
          ```

          ---

          ## Quick Start (MacBook / Linux Workstation)

          ### 1. Clone the Repository
          ```bash
          git clone https://github.com/YOUR_GITHUB_USERNAME/lakehouse-prototype.git
          cd lakehouse-prototype
          ```

          ### 2. Create a KIND Cluster
          ```bash
          kind create cluster --config kind-config.yaml
          ```

          ### 3. Deploy All Components
          ```bash
          make apply-all
          ```

          ### 4. Upload a Sample CSV to MinIO
          - Open MinIO Console: http://localhost:30000
          - Login with: `minioadmin` / `minioadmin`
          - Create a bucket: `bucket_name`
          - Upload a CSV file at `cts_output/sample.csv`

          ### 5. Send Message to Kafka
          ```bash
          make send-msg
          ```
          This sends a structured Kafka message like:
          ```json
          {
            "instruction": "load data to delta table",
            "source_path": "s3a://bucket_name/cts_output/sample.csv",
            "delta_path": "s3a://bucket_name/cts_payload/delta/events",
            "namespace": "CTS_Payload",
            "table_name": "cts_job_results",
            "job_id": "job_001"
          }
          ```

          ### 6. Run Spark Job
          ```bash
          make run-job
          ```

          ### 7. Launch JupyterHub
          - URL: http://localhost:30088
          - Use a notebook to connect to Spark and read the Delta table:

          ```python
          from pyspark.sql import SparkSession
          spark = SparkSession.builder.getOrCreate()
          df = spark.read.format("delta").load("s3a://bucket_name/cts_payload/delta/events")
          df.show()
          ```

          ---

          ## Tear Down

          ```bash
          make delete-cluster
          ```

          ---

          ## ⚙️ Customization & Environment Variables

          - MinIO credentials are read from `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY`
          - You can override default settings in the Spark job or Kafka script using `.env` or shell exports.

          ```bash
          export MINIO_ACCESS_KEY=mykey
          export MINIO_SECRET_KEY=mysecret
          ```

          ---

          ## Use Cases Demonstrated

          - Real-time file-based ingestion via Kafka
          - Delta Lake table creation and incremental append
          - Interactive notebook-driven lakehouse exploration
          - Fully local, reproducible, and containerized workflow

          ---

          ## License
          MIT

          ---

          _Built for engineers, researchers, and data professionals exploring modern data architecture on laptops._
