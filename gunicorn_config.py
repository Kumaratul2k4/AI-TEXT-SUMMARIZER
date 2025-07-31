# gunicorn_config.py

workers = 2

# The socket to bind to.
# '0.0.0.0' makes the server accessible from any IP address.
bind = "0.0.0.0:8000"

# Timeout for handling a request (in seconds)
timeout = 120

# Log level
loglevel = "info"

preload_app = True
