"""Sentiment analysis API that serves a model from the W&B Registry.

How it works:
1. On startup, the app asks W&B which model version the alias (e.g. "latest") points to,
   downloads it into model/<version>, and loads it into memory.
2. A background task re-checks the alias every POLL_INTERVAL_SECONDS. When someone links a new
   version in W&B and the alias moves, the app downloads and loads it, then swaps it in.
   No restart is needed and requests keep being served during the update.
3. /predict always uses whichever model is currently loaded.
"""

import asyncio
import logging
import os
import shutil
from contextlib import asynccontextmanager
from pathlib import Path

import wandb
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Read settings from the .env file into environment variables (WANDB_API_KEY, MODEL_NAME, ...)
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
MODEL_NAME = os.getenv("MODEL_NAME")  # moizasghar-afiniti-org/wandb-registry-latest-sentiment-model/bert-tiny
MODEL_ALIAS = os.getenv("VERSION", "latest")  # an alias (latest/production) enables hot reload; a fixed "v0" never changes
POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))  # 0 disables background polling

MODELS_DIR = Path("model")  # one sub-directory per W&B version, e.g. model/v3

# ---------------------------------------------------------------------------
# Global state, shared by all requests
# ---------------------------------------------------------------------------
classifier = None  # the loaded Hugging Face pipeline; None until the first successful load
model_info = {}  # details about the loaded model; its "digest" is how we detect a new version


# ---------------------------------------------------------------------------
# Request / response schemas (FastAPI validates these automatically)
# ---------------------------------------------------------------------------
class TextInput(BaseModel):
    text: str

class PredictionResponse(BaseModel):
        text: str
        label: str
        score: float
        confidence_percentage: float


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------
def build_classifier(model_path: Path):
    """Load the model weights and tokenizer from disk and wrap them in a ready-to-use pipeline."""
    model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)


def sync_with_wandb() -> bool:
    """Download and load the model the alias points to, if it differs from the loaded one.

    Runs in a worker thread so the event loop keeps serving requests during the download.
    Returns True if a new model was swapped in.
    """
    global classifier, model_info

    # Ask W&B which version the alias points to right now. This only fetches metadata, not the files.
    # Authentication uses the WANDB_API_KEY environment variable.
    artifact = wandb.Api().artifact(f"{MODEL_NAME}:{MODEL_ALIAS}")

    # The digest is a fingerprint of the artifact's contents: same digest means same model, so do nothing
    if artifact.digest == model_info.get("digest"):
        return False

    # New version: download it into its own folder (e.g. model/v3) and load it.
    # The current model keeps serving requests while this happens.
    model_path = Path(artifact.download(root=str(MODELS_DIR / artifact.version)))
    new_classifier = build_classifier(model_path)

    old_path = model_info.get("model_path")
    # Single assignment swap: in-flight requests finish on the old model, new ones use the new model
    classifier = new_classifier
    model_info = {
        "model_path": str(model_path),
        "source": f"{MODEL_NAME}:{MODEL_ALIAS}",
        "version": artifact.version,
        "digest": artifact.digest,
        "num_labels": 2,
        "labels": ["Negative", "Positive"],
    }
    logger.info(f"Loaded model {artifact.version} ({artifact.digest[:8]}) from {model_path}")

    # The old model is already in memory, so its files are no longer needed
    if old_path and old_path != str(model_path):
        shutil.rmtree(old_path, ignore_errors=True)
    return True


async def poll_for_updates():
    """Background loop: every POLL_INTERVAL_SECONDS, check W&B for a new model version."""
    while True:
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
        try:
            # asyncio.to_thread runs the slow, blocking download/load outside the event loop,
            # so /predict and the other endpoints stay responsive
            await asyncio.to_thread(sync_with_wandb)
        except Exception as e:
            # A failed check (network error, W&B down, ...) is not fatal: keep serving the current model
            logger.error(f"Model update check failed, keeping current model: {e}")


# ---------------------------------------------------------------------------
# App lifecycle: code before `yield` runs on startup, code after it runs on shutdown
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load the initial model
    try:
        await asyncio.to_thread(sync_with_wandb)
    except Exception as e:
        # The poller keeps retrying, so the model loads once W&B is reachable
        logger.error(f"Failed to load model on startup: {e}")

    # Start the background update checker (it runs alongside the API)
    poller = asyncio.create_task(poll_for_updates()) if POLL_INTERVAL_SECONDS > 0 else None
    yield  # the app serves requests while paused here
    # Shutdown: stop the background checker
    if poller:
        poller.cancel()


app = FastAPI(title="Sentiment Analysis API", version="1.0", lifespan=lifespan)

# Allow the frontend (served from a different origin/port) to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # * allows all origins, you can specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/") # http://127.0.0.1:8000/
async def root():
    # Shows which model version is being served, handy for confirming an update went live
    return {
        "message": "Sentiment Analysis API is running.",
        "model_info": model_info,
        "model_loaded": classifier is not None
    }

@app.get("/health") # http://127.0.0.1:8000/health
async def health_check():
    # Returns 503 until a model is loaded, so Docker/load balancers know the app isn't ready yet
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse) # http://127.0.0.1:8000/predict
async def predict(input: TextInput):
    current = classifier  # hold one reference so a mid-request swap can't change the model under us
    if current is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        # The pipeline returns a list with one result per input: [{"label": <predicted class>, "score": <0-1>}]
        result = current(input.text)

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

# Run with `python app.py`. reload=True restarts the server when .py files change (development only)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
