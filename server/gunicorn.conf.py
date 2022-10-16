wsgi_app = "app:app"
workers = 8
worker_class = "uvicorn.workers.UvicornWorker"
bind = "0.0.0.0:5000"
accesslog = "app.log"
loglevel = "info"
daemon = True
