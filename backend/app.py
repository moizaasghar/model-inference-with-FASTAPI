from importlib import reload
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analysis API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and tokenizer
classifier = None
model_info = {}

class TextInput(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    text: str
    label: str
    score: float
    confidence_percentage: float

def load_model():
    """Load the sentiment analysis model"""
    global classifier, model_info
    
    try:
        # First, try to load from downloaded W&B model
        model_path = "model"  # W&B downloaded model
        
        if not model_path:
            raise FileNotFoundError("Model not found in any expected location")
        
        # Load model and tokenizer
        model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Create pipeline
        classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
        
        # Store model info
        model_info = {
            "model_path": model_path,
            "num_labels": 2,
            "labels": ["Negative", "Positive"]
        }
        
        logger.info("Model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    success = load_model()
    if not success:
        logger.error("Failed to load model on startup")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Sentiment Analysis API is running!",
        "model_loaded": classifier is not None,
        "model_info": model_info
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict_sentiment(input_data: TextInput):
    """Predict sentiment for given text"""
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Get prediction
        result = classifier(input_data.text)
        
        # Extract result (pipeline returns a list with one dict)
        prediction = result[0]
        label = prediction['label']
        score = prediction['score']
        confidence_percentage = round(score * 100, 2)
        
        return PredictionResponse(
            text=input_data.text,
            label=label,
            score=score,
            confidence_percentage=confidence_percentage
        )
        
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
