#!/usr/bin/env bash

bash modelapp/bootstrap-python-env.sh && . modelapp-python-env/bin/activate && python3 modelapp/src/modelapp/train.py
docker build -t mytest .
docker run -d -p 8080:8080 mytest