#!/bin/bash

# Backend startup script

echo "🚀 Starting Sentiment Analysis Backend..."

# Download model from W&B
echo "🤖 Downloading model from W&B..."
python setup.py

# Start the FastAPI application
echo "🔥 Starting FastAPI server..."
python app.py
