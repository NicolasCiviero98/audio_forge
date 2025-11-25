import os
import tempfile
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

from pydub import AudioSegment
from app.services.storage_service import download_audio, load_audio_bytes

INTRO_FILENAME = "INTRO.mp3"


def _create_temp_file(suffix: str) -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    return path


def _bytes_to_audiosegment(audio_bytes: bytes) -> AudioSegment:
    return AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")


def _encode_to_mp3(input_wav: str, output_mp3: str):
    """
    WhatsApp-safe MP3 encoding.
    """
    cmd = [
        "ffmpeg", "-y",
        "-i", input_wav,
        "-ar", "44100",
        "-ac", "2",
        "-codec:a", "libmp3lame",
        "-b:a", "128k",
        "-write_xing", "0",
        output_mp3
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _load_segment(gcs_path: str):
    audio_bytes = load_audio_bytes(gcs_path)
    return _bytes_to_audiosegment(audio_bytes)


# MAIN AUDIO BUILDER
def build_audio_file(category_folder: str, items: list[str]) -> tuple[str, int]:
    final_audio = AudioSegment.silent(duration=0)

    # Build list of all paths (intro + items)
    paths = [f"{category_folder}/{INTRO_FILENAME}"] + \
            [f"{category_folder}/{item}.mp3" for item in items]

    start = time.perf_counter()
    # Load all AUDIOSEGMENTS IN PARALLEL (max workers = number of files or CPU count)
    with ThreadPoolExecutor(max_workers=8) as executor:
        segments = list(executor.map(_load_segment, paths))
    elapsed = time.perf_counter() - start
    print(f"TOTAL: {elapsed:.4f} seconds")

    # Merge segments in the correct order
    for segment in segments:
        final_audio += segment

    # Export WAV + encode MP3 (unchanged)
    wav_path = _create_temp_file(".wav")
    final_audio.export(wav_path, format="wav")

    mp3_path = _create_temp_file(".mp3")
    _encode_to_mp3(wav_path, mp3_path)

    try:
        os.remove(wav_path)
    except FileNotFoundError:
        pass

    return mp3_path, len(final_audio)
