# syntax=docker/dockerfile:1

# Use an official Python image based on Debian Bullseye
FROM python:3.8-slim-bullseye

# ---------------------------------------------------------------------------
# Global environment
# ---------------------------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=1200 \
    PIP_RETRIES=10

# ---------------------------------------------------------------------------
# System dependencies required to build many Python wheels
# ---------------------------------------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        build-essential \
        libffi-dev \
        libssl-dev \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------------
# Working directory
# ---------------------------------------------------------------------------
WORKDIR /app

# ---------------------------------------------------------------------------
# Install Python dependencies
# ---------------------------------------------------------------------------
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt && \
    pip install --no-cache-dir --prefer-binary "langchain-serve[api]"

# ---------------------------------------------------------------------------
# Copy application source
# ---------------------------------------------------------------------------
COPY . .

# ---------------------------------------------------------------------------
# Entrypoint script
# ---------------------------------------------------------------------------
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && \
    mkdir -p /var/log && \
    touch /var/log/app.log

# ---------------------------------------------------------------------------
# Expose the service port (Gradio)
# ---------------------------------------------------------------------------
EXPOSE 7860

# ---------------------------------------------------------------------------
# Container start command
# ---------------------------------------------------------------------------
CMD ["/entrypoint.sh"]
