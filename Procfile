web: AGENT_PORT=$PORT python main.py
worker: celery -A core.celery_app worker --loglevel=info
