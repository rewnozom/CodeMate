# Project Details

# Table of Contents
- [..\docker\Dockerfile](#-docker-Dockerfile)
- [..\docker\Dockerfile.dev](#-docker-Dockerfiledev)
- [..\docker\Dockerfile.prod](#-docker-Dockerfileprod)
- [..\docker\__init__.py](#-docker-__init__py)


# ..\..\docker\Dockerfile
## File: ..\..\docker\Dockerfile

```
# ..\..\docker\Dockerfile
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
```

---

# ..\..\docker\Dockerfile.dev
## File: ..\..\docker\Dockerfile.dev

```dev
# ..\..\docker\Dockerfile.dev
# docker/Dockerfile.dev
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/dev.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Start development server
CMD ["python", "src/main.py", "start", "--debug"]



```

---

# ..\..\docker\Dockerfile.prod
## File: ..\..\docker\Dockerfile.prod

```prod
# ..\..\docker\Dockerfile.prod
# docker/Dockerfile.prod
FROM python:3.10-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/prod.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create production image
FROM python:3.10-slim

WORKDIR /app

# Copy from builder
COPY --from=builder /app/src ./src
COPY --from=builder /app/config ./config
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m agent
USER agent

# Start application
CMD ["python", "src/main.py", "start"]

```

---

# ..\..\docker\__init__.py
## File: ..\..\docker\__init__.py

```py
# ..\..\docker\__init__.py
# Auto-generated __init__.py file

```

---

