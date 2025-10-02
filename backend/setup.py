import os
import wandb
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def download_model_from_wandb():
    api_key = os.getenv("WANDB_API_KEY")

    wandb.login(key=api_key)

    api = wandb.Api()

    models_dir = Path("model")
    models_dir.mkdir(exist_ok=True)

    try: 
        model_name = os.getenv("MODEL_NAME")
        version = os.getenv("VERSION")
        
        model_uri = f"{model_name}:{version}"
        print(model_uri)

        model_artifact = api.artifact(model_uri)
        model_artifact_dir = model_artifact.download(root="model/")

        print(f"Model downloaded @ {model_artifact_dir}")

    except Exception as e:
        print(f"Error while downloading the model: {e}")



if __name__ == "__main__":
    download_model_from_wandb()
   