import os
import tempfile
from google.cloud import storage
from app.core.config import BUCKET_NAME, AUDIO_PROVIDER

# GOOGLE CLOUD STORAGE CLIENT
gcs_client = storage.Client()
bucket = gcs_client.bucket(BUCKET_NAME)


def load_audio_bytes(gcs_or_local_path: str) -> bytes:
    if AUDIO_PROVIDER == "local":
        return load_local_file_bytes(gcs_or_local_path)
    else:
        return load_gcs_file_bytes(gcs_or_local_path)


def load_local_file_bytes(rel_path: str) -> bytes:
    full_path = f"app/audio_assets/{rel_path}"
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Local audio file not found: {full_path}")
    with open(full_path, "rb") as f:
        return f.read()


def load_gcs_file_bytes(rel_path: str) -> bytes:
    full_path = f"audio/{rel_path}"
    blob = bucket.blob(full_path)

    if not blob.exists():
        raise FileNotFoundError(f"GCS audio file not found: {full_path}")

    return blob.download_as_bytes()


# DOWNLOAD FILE FROM STORAGE
def download_audio(gcs_path: str) -> str:
    """
    Downloads a file from Google Cloud Storage into a temporary local file.
    Returns the temporary file path.
    """
    blob = bucket.blob(gcs_path)

    if not blob.exists():
        raise FileNotFoundError(f"Audio file not found: {gcs_path}")

    fd, tmp_path = tempfile.mkstemp()
    os.close(fd)

    blob.download_to_filename(tmp_path)
    return tmp_path


# DEBUG HELPERS
def test_file(path: str) -> dict:
    """
    Debug: checks if a given path exists inside the bucket.
    """
    full_path = f"audio/{path}"
    blob = bucket.blob(full_path)

    return {
        "tested": full_path,
        "exists": blob.exists(),
        "size": blob.size if blob.exists() else None
    }


def list_audio_files(prefix="audio/") -> list:
    """
    Returns a list of all audio files under /audio for debugging.
    """
    return [blob.name for blob in bucket.list_blobs(prefix=prefix)]
