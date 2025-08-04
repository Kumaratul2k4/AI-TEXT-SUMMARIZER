import os

# Set number of workers — 1 is best for free/low-memory hosting
workers = 1

# Bind to dynamic port (Heroku, Replit, etc.) or fallback to localhost:8000
port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Increase timeout for large model loading or slow responses
timeout = 120

# Set logging level
loglevel = "info"

# Load the app before forking worker processes
preload_app = True
