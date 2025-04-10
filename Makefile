CLUSTER_NAME=lakehouse-demo

create-cluster:
	kind create cluster --name $(CLUSTER_NAME) --config kind-config.yaml

delete-cluster:
	kind delete cluster --name $(CLUSTER_NAME)

apply-all:
	kubectl apply -f manifests/minio/
	kubectl apply -f manifests/kafka/
	kubectl apply -f manifests/spark/
	kubectl apply -f manifests/jupyterhub/

run-job:
	kubectl apply -f manifests/spark/spark-job.yaml

send-msg:
	python scripts/send_kafka_message.py
