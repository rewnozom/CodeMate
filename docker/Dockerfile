# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements/prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY config/ config/
COPY scripts/ scripts/

# Create necessary directories
RUN mkdir -p logs temp workspace

# Set Python path
ENV PYTHONPATH=/app

# Set default command
CMD ["python", "src/main.py", "start"]