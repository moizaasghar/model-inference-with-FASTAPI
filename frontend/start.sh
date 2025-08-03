#!/bin/bash

# Frontend startup script

echo "🎭 Starting Sentiment Analysis Frontend..."

# Start Streamlit application
echo "🌟 Starting Streamlit server..."
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
