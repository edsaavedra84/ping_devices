# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Install system dependencies including ping
RUN apt-get update && \
    apt-get install -y --no-install-recommends iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ping_devices.py .

# Create directories for config and logs
RUN mkdir -p /app/config /app/logs

# Set environment variable to unbuffer Python output
ENV PYTHONUNBUFFERED=1

# Volume mounts for config and logs
VOLUME ["/app/config", "/app/logs"]

# Run the application
CMD ["python", "ping_devices.py"]
