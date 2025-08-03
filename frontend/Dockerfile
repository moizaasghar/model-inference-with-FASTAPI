# Frontend Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend application
COPY . .

# Make script executable
RUN chmod +x start.sh

# Expose Streamlit port
EXPOSE 8501

# Use the start script as entry point
CMD ["./start.sh"]
