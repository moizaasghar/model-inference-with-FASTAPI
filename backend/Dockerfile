# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# The app downloads the model from W&B on startup
CMD ["python", "app.py"]
