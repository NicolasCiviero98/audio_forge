from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.models.audio_report_request import AudioReportRequest
from app.services.audio_service import build_audio_file

router = APIRouter()

@router.post("/")
def forge_audio(req: AudioReportRequest):
    try:
        mp3_path, duration_ms = build_audio_file(req.category, req.items)

        return FileResponse(
            path=mp3_path,
            media_type="audio/mpeg",
            filename="audioforge_output.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
