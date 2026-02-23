#!/usr/bin/env bash
set -e

# Start the Gradio frontend (PDF GPT app)
# Note: This app requires lcserve API backend which may not be available
# For now, we start the Gradio app directly
echo "Starting Gradio PDF GPT on port 7860..."
python /app/app.py
