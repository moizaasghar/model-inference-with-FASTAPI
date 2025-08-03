# Sentiment Analysis with FastAPI and Streamlit

A complete sentiment analysis application using a fine-tuned BERT model, served via FastAPI backend with a beautiful Streamlit frontend.

## 🚀 Features

- **FastAPI Backend**: RESTful API for sentiment analysis
- **Streamlit Frontend**: Interactive web interface
- **BERT Model**: Fine-tuned on IMDb dataset
- **W&B Integration**: Model loading from Weights & Biases registry
- **Docker Support**: Containerized deployment
- **Batch Processing**: Analyze multiple texts at once
- **Real-time Predictions**: Instant sentiment analysis

## 📁 Project Structure

```
model-inference-with-FASTAPI/
├── backend/                    # FastAPI backend service
│   ├── app.py                 # Main FastAPI application
│   ├── setup.py               # W&B model download script
│   ├── start.sh               # Backend startup script
│   ├── requirements.txt       # Backend dependencies
│   ├── docker/
│   │   └── Dockerfile         # Backend Docker configuration
│   ├── models/                # Downloaded models (auto-created)
│   └── README.md              # Backend documentation
├── frontend/                   # Streamlit frontend service
│   ├── app.py                 # Main Streamlit application
│   ├── start.sh               # Frontend startup script
│   ├── requirements.txt       # Frontend dependencies
│   ├── docker/
│   │   └── Dockerfile         # Frontend Docker configuration
│   └── README.md              # Frontend documentation
├── docker-compose.yml          # Docker orchestration
└── README.md                  # This file (overview)
```

## 🛠️ Quick Start

### Docker Deployment (Recommended)

1. **Clone and navigate to the project directory**
2. **Start all services:**
   ```bash
   docker-compose up --build
   ```
3. **Access the applications:**
   - Frontend (Streamlit): http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python setup.py  # Download model from W&B
python app.py    # Start FastAPI server
```

#### Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py  # Start Streamlit app
```

## 🔧 Configuration

### W&B Model Registry

Update your W&B credentials in `backend/setup.py`:

```python
# Your W&B API key
api_key = "your_wandb_api_key"

# Your model artifact path
artifact = api.artifact("username/project/model-name:latest")
```

### API Configuration

For local development, update the API URL in `frontend/app.py`:

```python
API_BASE_URL = "http://localhost:8000"  # For local development
```

## 📊 API Endpoints

### Health Check
- **GET** `/health` - Check API status

### Single Prediction
- **POST** `/predict`
  ```json
  {
    "text": "I love this movie!"
  }
  ```

### Batch Prediction
- **POST** `/batch_predict`
  ```json
  ["Text 1", "Text 2", "Text 3"]
  ```

## 🎯 Usage Examples

### Single Text Analysis
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "This movie is amazing!"}
)
print(response.json())
```

### Batch Analysis
```python
texts = [
    "I love this product!",
    "This is terrible.",
    "It's okay, nothing special."
]

response = requests.post(
    "http://localhost:8000/batch_predict",
    json=texts
)
print(response.json())
```

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

## 📈 Model Information

- **Base Model**: `prajjwal1/bert-tiny`
- **Task**: Binary sentiment classification
- **Labels**: Positive, Negative
- **Training Dataset**: IMDb movie reviews
- **Framework**: Hugging Face Transformers

## 🔍 Frontend Features

1. **Single Text Analysis**: Analyze individual texts with confidence scores
2. **Batch Processing**: Upload text files or paste multiple texts
3. **Example Gallery**: Pre-loaded examples to test the model
4. **Real-time Status**: API health monitoring
5. **Beautiful UI**: Clean, responsive design with progress indicators

## 🚨 Troubleshooting

### Model Loading Issues
- Ensure W&B credentials are correct in `backend/setup.py`
- Check if the model artifact exists in your W&B registry
- Verify the fallback model path is accessible

### API Connection Issues
- Make sure the backend is running on port 8000
- Check firewall settings
- Verify Docker containers are healthy: `docker-compose ps`

### Docker Issues
- Ensure Docker and Docker Compose are installed
- Check available disk space for model download
- Verify ports 8000 and 8501 are not in use

## 📋 Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Streamlit     │◄───────────────►│   FastAPI       │
│   Frontend      │                 │   Backend       │
│   (Port 8501)   │                 │   (Port 8000)   │
└─────────────────┘                 └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │   BERT Model    │
                                    │   (W&B/Local)   │
                                    └─────────────────┘
```

## 🔒 Security Considerations

- Store W&B API keys in environment variables for production
- Configure specific CORS origins instead of "*" in production
- Implement rate limiting for production use
- Use HTTPS in production environments

## 📝 Documentation

- **Backend Details**: See `backend/README.md`
- **Frontend Details**: See `frontend/README.md`
- **API Documentation**: Available at http://localhost:8000/docs when running

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📧 Support

For issues and questions, please open an issue in the GitHub repository.
