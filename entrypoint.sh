#!/usr/bin/env bash
set -e

# Start the langchain-serve API backend
echo "Starting langchain-serve API on port 8080..."
python -m lcserve api --port 8080 --host 0.0.0.0 &

# Wait for the API to be ready
sleep 5

# Start the Gradio frontend (PDF GPT app)
echo "Starting Gradio PDF GPT on port 7860..."
python /app/app.py

