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
│   ├── requirements.txt       # Backend dependencies
│   ├── Dockerfile              # Backend Docker configuration
│   ├── model/                 # Downloaded model versions (auto-created)
│   └── README.md              # Backend documentation
├── frontend/                   # Streamlit frontend service
│   ├── app.py                 # Main Streamlit application
│   ├── start.sh               # Frontend startup script
│   ├── requirements.txt       # Frontend dependencies
│   ├── Dockerfile              # Frontend Docker configuration
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
5. **Responsive UI**: Clean, responsive design with progress indicators


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

