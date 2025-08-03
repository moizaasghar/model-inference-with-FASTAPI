# FastAPI Backend for Sentiment Analysis

This is the backend service that serves the BERT sentiment analysis model via a RESTful API.

## 🚀 Features

- **FastAPI Framework**: High-performance, easy-to-use web framework
- **BERT Model Integration**: Fine-tuned BERT model for sentiment analysis
- **W&B Model Loading**: Automatic model download from Weights & Biases registry
- **RESTful API**: Clean endpoints for single and batch predictions
- **Docker Support**: Containerized deployment ready
- **Health Monitoring**: Built-in health check endpoints
- **CORS Support**: Cross-origin requests enabled for frontend integration

## 📁 Structure

```
backend/
├── app.py                  # Main FastAPI application
├── setup.py               # W&B model download script
├── start.sh               # Startup script (Docker entrypoint)
├── requirements.txt       # Python dependencies
├── Dockerfile              # Docker configuration
├── models/                # Downloaded models (created automatically)
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download model from W&B:**
   ```bash
   python setup.py
   ```

3. **Start the server:**
   ```bash
   python app.py
   # Or use the startup script
   ./start.sh
   ```

### Docker Deployment

```bash
# Build the image
docker build -t sentiment-backend .

# Run the container
docker run -p 8000:8000 sentiment-backend
```

## 📊 API Endpoints

### Health Check
- **GET** `/health` - Check if the API is running and model is loaded
- **GET** `/` - Basic API information

### Predictions
- **POST** `/predict` - Single text prediction
  ```json
  {
    "text": "I love this movie!"
  }
  ```

## 🔧 Configuration

### W&B Settings
Update your W&B credentials in `setup.py`:

```python
# Your W&B API key
api_key = "your_wandb_api_key"

# Your model artifact path
artifact = api.artifact("username/project/model-name:latest")
```

### Model Paths
The application tries to load models from these locations (in order):
1. `models/bert-tiny-imdb` (downloaded from W&B)
2. `models/artifacts/bert-tiny-sentiment-model:v0/bert-tiny-imdb`
3. Fallback local path (configurable in setup.py)

## 📝 Usage Examples

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"text\": \"This movie is amazing!\"}"
```