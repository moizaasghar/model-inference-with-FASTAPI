# FastAPI Backend for Sentiment Analysis

This is the backend service that serves the BERT sentiment analysis model via a RESTful API.

## 🚀 Features

- **FastAPI Framework**: High-performance, easy-to-use web framework
- **BERT Model Integration**: Fine-tuned BERT model for sentiment analysis
- **W&B Model Loading**: Downloads the model from the Weights & Biases registry on startup
- **Hot Model Updates**: Polls the registry alias and swaps in new versions without a restart
- **RESTful API**: Clean endpoints for single and batch predictions
- **Docker Support**: Containerized deployment ready
- **Health Monitoring**: Built-in health check endpoints
- **CORS Support**: Cross-origin requests enabled for frontend integration

## 📁 Structure

```
backend/
├── app.py                  # Main FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile              # Docker configuration
├── model/                 # Downloaded model versions, e.g. model/v3 (created automatically)
└── README.md             # This file
```

## 🛠️ Installation & Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server** (downloads the model from W&B on startup):
   ```bash
   python app.py
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

Set these in `.env` (or as environment variables):

| Variable | Description |
|---|---|
| `WANDB_API_KEY` | Your W&B API key |
| `MODEL_NAME` | Registry path, e.g. `org/wandb-registry-model/bert-tiny` |
| `VERSION` | Alias or version to serve. Use an alias (`latest`, `production`) to get automatic updates; a fixed version like `v0` never changes |
| `POLL_INTERVAL_SECONDS` | How often to check the alias for a new version (default `60`, `0` disables) |

### Automatic model updates
Every `POLL_INTERVAL_SECONDS`, the app checks which version the alias points to. If the digest changed, it downloads the new version to `model/<version>`, loads it, and swaps it in without a restart. The old version's files are deleted. `GET /` shows the version currently being served.

## 📝 Usage Examples

### Using curl
```bash
# Health check
curl http://localhost:8000/health

# Single prediction
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"text\": \"This movie is amazing!\"}"
```