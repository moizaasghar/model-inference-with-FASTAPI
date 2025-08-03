#!/bin/bash

# Frontend startup script

echo "🎭 Starting Sentiment Analysis Frontend..."

# Start Streamlit application
echo "🌟 Starting Streamlit server..."
streamlit run app.py --server.address "${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}" --server.port "${STREAMLIT_SERVER_PORT:-8501}"
