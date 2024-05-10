#!/bin/sh
sudo docker-compose up --build
cd inference-service
sudo docker run --name inference-service --gpus all --rm -p 8000:8000 -p 8001:8001 -p 8002:8002 -v ${PWD}/model_repository:/models nvcr.io/nvidia/tritonserver:24.04-py3 tritonserver --model-repository=/models
sudo docker network connect ml-cryptostock_postgres-network inference-service
