#!/usr/bin/env bash

python3 modelapp/src/modelapp/train
docker build -t mytest .
docker run -it -p 8080:8080 mytest