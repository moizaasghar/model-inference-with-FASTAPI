import os
import wandb
import zipfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def download_model_from_wandb():
    """
    Download the trained model from W&B model registry
    """
    # Your W&B API key
    api_key = os.getenv("WANDB_API_KEY")
    
    # Login to W&B
    wandb.login(key=api_key)
    
    # Initialize W&B API
    api = wandb.Api()
    
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    try:
        # Download the model artifact
        # Replace with your actual W&B username/project and artifact name
        model_name = os.getenv("MODEL_NAME")
        version = os.getenv("VERSION")
        model_uri = f"{model_name}:{version}"
        print(f"Model URI: {model_uri}")
        artifact = api.artifact(model_uri)

        # Download to local directory
        artifact_dir = artifact.download(root="model/")
        
        print(f"Model downloaded successfully to: {artifact_dir}")
   
    except Exception as e:
        print(f"Error downloading model from W&B: {e}")

if __name__ == "__main__":
    model_path = download_model_from_wandb()

