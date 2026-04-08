web: uvicorn api.gateway:app --host 0.0.0.0 --port $PORT
worker: celery -A core.celery_app worker --loglevel=info
