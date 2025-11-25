# app/models/audio_report_request.py

from pydantic import BaseModel, field_validator
from typing import List

class AudioReportRequest(BaseModel):
    """
    Represents the request payload for generating an audio report.
    Includes:
      - category: the audio group (e.g., florais_bach)
      - items: list of audio item names inside that category
    """
    category: str
    items: List[str]

    @field_validator("category")
    def validate_category(cls, v):
        if not v or not v.strip():
            raise ValueError("Category must be a non-empty string.")
        return v

    @field_validator("items")
    def validate_items(cls, v):
        if not v or len(v) == 0:
            raise ValueError("Items list cannot be empty.")
        return v
