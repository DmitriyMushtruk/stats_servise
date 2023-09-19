#!/bin/bash

uvicorn app.main:app --host 0.0.0.0 --port 8090 --reload &

python app/consumer.py


exec "$@"