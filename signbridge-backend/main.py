import time
import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from models import HealthResponse, TranscriptionResponse
from transcriber import AudioTranscriptionService, AudioDecodingError

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("signbridge.server")

start_time = time.time()
transcription_service: Optional[AudioTranscriptionService] = None
latest_transcription: Optional[TranscriptionResponse] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global transcription_service
    logger.info("Initializing SignBridge Speech Recognition Service...")
    transcription_service = AudioTranscriptionService()
    logger.info(f"SignBridge backend ready on http://{settings.host}:{settings.port}")
    yield
    logger.info("Shutting down SignBridge Speech Recognition Service...")

app = FastAPI(
    title="SignBridge Speech Recognition Service",
    description="Local zero-cost speech-to-text service powered by faster-whisper",
    version="0.2.0",
    lifespan=lifespan
)

# Enable CORS for Chrome extension origins
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"chrome-extension://.*|http://127\.0\.0\.1.*|http://localhost.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify local backend status and model readiness."""
    return HealthResponse(
        status="ok",
        service="signbridge-backend",
        version="0.2.0",
        model=settings.model_name,
        device=settings.device,
        compute_type=settings.compute_type,
        uptime_seconds=round(time.time() - start_time, 1)
    )

@app.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    audio: UploadFile = File(..., description="Audio slice (WebM, WAV, OGG, etc.)"),
    sequence_id: int = Form(0, description="Sequential chunk counter"),
    timestamp: float = Form(0.0, description="Elapsed playback timestamp (seconds)"),
    language: Optional[str] = Form(None, description="Optional target language (e.g. 'en')")
):
    """
    Transcribe a stream audio chunk into timestamped segments.
    Audio is decoded completely in memory; no audio is written to disk or sent externally.
    """
    if not transcription_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Transcription engine is not yet initialized"
        )

    # 1. Read audio bytes
    audio_bytes = await audio.read()
    byte_size = len(audio_bytes)

    # 2. Validate request limits (PRD Section 13 / Error Handling)
    if byte_size > settings.max_audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"Audio payload size ({byte_size} bytes) exceeds limit ({settings.max_audio_bytes} bytes)"
        )

    if byte_size == 0:
        logger.warning(f"Received empty audio chunk (sequence_id={sequence_id})")
        return TranscriptionResponse(
            status="empty",
            sequence_id=sequence_id,
            timestamp=timestamp,
            duration=0.0,
            language="unknown",
            language_probability=0.0,
            text="",
            segments=[],
            metrics={"inference_time_ms": 0.0, "rtf": 0.0, "audio_bytes": 0}
        )

    # 3. Transcribe audio in memory
    try:
        lang = language or settings.default_language
        result = transcription_service.transcribe_audio_bytes(
            audio_bytes=audio_bytes,
            sequence_id=sequence_id,
            timestamp=timestamp,
            language=lang
        )

        logger.info(
            f"Chunk #{sequence_id} transcribed: duration={result.duration}s, "
            f"inference={result.metrics.inference_time_ms}ms, RTF={result.metrics.rtf}, "
            f"words={len(result.segments)}"
        )
        global latest_transcription
        latest_transcription = result
        return result

    except AudioDecodingError as err:
        logger.error(f"Invalid audio format in chunk #{sequence_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except Exception as err:
        logger.error(f"Unexpected error transcribing chunk #{sequence_id}: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal transcription error"
        )

@app.get("/api/transcript/latest")
async def get_latest_transcript():
    """Retrieve the latest transcribed chunk for local overlay viewers."""
    if latest_transcription is None:
        return {"status": "waiting", "text": "", "sequence_id": -1}
    return latest_transcription


