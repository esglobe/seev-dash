import os

port = os.environ["PORT"]
bind = f'0.0.0.0:{port}'
workers = 4
worker_class = 'gevent'
worker_connections = 1000
keepalive = 5
accesslog = '-'
errorlog  = '-'