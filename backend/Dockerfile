# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Use the start script as entry point
CMD ["./start.sh"]
