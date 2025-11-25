import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ENVIRONMENT VARIABLES
BUCKET_NAME = os.getenv("GCS_BUCKET")
AUDIO_PROVIDER = os.getenv("AUDIO_PROVIDER")

required_vars = {
    "GCS_BUCKET": BUCKET_NAME,
    "AUDIO_PROVIDER": AUDIO_PROVIDER,
}

missing = [name for name, value in required_vars.items() if not value]

if missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")


