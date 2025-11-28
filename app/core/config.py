import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ENVIRONMENT VARIABLES
BUCKET_NAME = os.getenv("GCS_BUCKET")
AUDIO_PROVIDER = os.getenv("AUDIO_PROVIDER")
CORS_ORIGINS = os.getenv("CORS_ORIGINS")

required_vars = {
    "GCS_BUCKET": BUCKET_NAME,
    "AUDIO_PROVIDER": AUDIO_PROVIDER,
    "CORS_ORIGINS": CORS_ORIGINS,
}

missing = [name for name, value in required_vars.items() if not value]

if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")


