from typing import List, Optional
from pydantic import BaseModel, Field

class WordItem(BaseModel):
    word: str
    start: float
    end: float
    probability: float

class SegmentItem(BaseModel):
    id: int
    start: float
    end: float
    text: str
    words: Optional[List[WordItem]] = Field(default_factory=list)

class TranscriptionMetrics(BaseModel):
    inference_time_ms: float
    rtf: float
    audio_bytes: int

class TranscriptionResponse(BaseModel):
    status: str = "ok" # "ok" | "empty" | "error"
    sequence_id: int = 0
    timestamp: float = 0.0
    duration: float = 0.0
    language: str = "en"
    language_probability: float = 1.0
    text: str = ""
    segments: List[SegmentItem] = Field(default_factory=list)
    metrics: TranscriptionMetrics
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "signbridge-backend"
    version: str = "0.2.0"
    model: str
    device: str
    compute_type: str
    uptime_seconds: float
