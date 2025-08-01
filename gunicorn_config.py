# gunicorn_config.py
import os

# 1. Reduced workers to 1 to save memory on free hosting plans.
workers = 1

# 2. Made the bind address dynamic to work with hosting platforms.
# It uses the PORT environment variable if available, otherwise defaults to 8000.
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Timeout for handling a request (in seconds)
timeout = 120

# Log level
loglevel = "info"

# Preloading the app can save some memory on startup.
preload_app = True
