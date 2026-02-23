# syntax=docker/dockerfile:1

# Use an official Python image based on Debian Bullseye
FROM python:3.10-slim

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
RUN pip install --upgrade pip && \
    # Install gradio and other packages (langchain-serve removed due to dependency conflicts)
    pip install --no-cache-dir --prefer-binary gradio openai litellm PyMuPDF numpy scikit-learn tensorflow tensorflow_hub wheel

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
