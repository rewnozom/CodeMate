# config/gunicorn.py
import multiprocessing

# Gunicorn config
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 50
reload = False
accesslog = "-"
errorlog = "-"
loglevel = "info"

# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream agent_server {
        server agent:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://agent_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}