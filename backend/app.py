from importlib import reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentiment Analysis API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    global classifier, model_info
    try:
        model_path = "model"

        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model directory '{model_path}' does not exist.")
        
        model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

        model_info = {
            "model_path": model_path,
            "num_labels": 2,
            "labels": ["Negative", "Positive"]
        }

        logger.info(f"Model loaded successfully from {model_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

@app.on_event("startup")
async def startup_event():
    success = load_model()
    if not success:
        logger.error("Failed to load model on startup.")
    else:
        logger.info("Model loaded and ready for predictions.")

@app.get("/")
async def root():
    return {
        "message": "Sentiment Analysis API is running.",
        "model_info": model_info,
        "model_loaded": classifier is not None
    }

@app.get("/health")
async def health_check():
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict(input: TextInput):
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        result = classifier(input.text)

        if not result:
            raise HTTPException(status_code=500, detail="Prediction failed")

        # Extract relevant information from the result
        label = result[0]['label']
        score = result[0]['score']
        confidence_percentage = round(score * 100, 2)

        return PredictionResponse(
            text=input.text,
            label=label,
            score=score,
            confidence_percentage=confidence_percentage
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)