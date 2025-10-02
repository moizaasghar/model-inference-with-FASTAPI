#!/bin/bash

echo "Starting Sentiment Analysis Backend..."

echo "Downloading the model..."
python setup.py

echo "Starting FastAPI server..."
python app.py