#!/bin/bash
alembic upgrade head
gunicorn src.main:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --forwarded-allow-ips="*"
