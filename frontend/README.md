# Streamlit Frontend for Sentiment Analysis

This is the frontend application that provides an interactive web interface for the sentiment analysis service.

## 🚀 Features

- **Interactive Web Interface**: Beautiful, responsive Streamlit application
- **Real-time Analysis**: Instant sentiment predictions with confidence scores
- **Batch Processing**: Analyze multiple texts simultaneously
- **File Upload Support**: Upload text files for batch analysis
- **Visual Feedback**: Progress bars, confidence indicators, and color coding
- **Example Gallery**: Pre-loaded examples for quick testing
- **API Health Monitoring**: Real-time backend status checking
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices

## 📁 Structure

```
frontend/
├── app.py                  # Main Streamlit application
├── start.sh               # Startup script (Docker entrypoint)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
└── README.md              # This file
```

## 🛠️ Installation & Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the application:**
   ```bash
   streamlit run app.py
   # Or use the startup script
   ./start.sh
   ```

### Docker Deployment

```bash
# Build the image
docker build -f docker/Dockerfile -t sentiment-frontend .

# Run the container
docker run -p 8501:8501 sentiment-frontend
```

## 🎯 Usage Guide

### Single Text Analysis
1. Navigate to the "🔍 Single Prediction" tab
2. Enter your text in the text area
3. Click "🚀 Analyze Sentiment"
4. View results with confidence scores and visual indicators

### Example Testing
1. Visit the "🧪 Examples" tab
2. Click "Analyze" on any pre-loaded example
3. See instant results for testing purposes

### Debug Mode
Enable Streamlit debug mode for development:
```bash
streamlit run app.py --logger.level debug
```