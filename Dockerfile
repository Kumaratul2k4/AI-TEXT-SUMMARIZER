# Use an official Python runtime as a parent image
# Using a specific version is good practice for reproducibility
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
# --no-cache-dir reduces image size
# The PyTorch download URL is for a CPU-only version, which is smaller
# and sufficient for many hosting plans (including Render's free tier).
RUN pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the rest of your application's code into the container
COPY . .

# Command to run the application using Gunicorn
# This will be executed when the container starts
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
