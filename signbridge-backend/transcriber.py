import io
import time
import logging
from typing import Optional, Tuple
from faster_whisper import WhisperModel
from config import settings
from models import TranscriptionResponse, SegmentItem, WordItem, TranscriptionMetrics

logger = logging.getLogger("signbridge.transcriber")

class AudioDecodingError(Exception):
    """Raised when the submitted audio format cannot be decoded."""
    pass

class AudioTranscriptionService:
    def __init__(self, model_name: str = None, compute_type: str = None, device: str = None, cpu_threads: int = None):
        self.model_name = model_name or settings.model_name
        self.compute_type = compute_type or settings.compute_type
        self.device = device or settings.device
        self.cpu_threads = cpu_threads or settings.cpu_threads
        self.model: Optional[WhisperModel] = None
        self._init_model()

    def _init_model(self):
        logger.info(
            f"Loading Whisper model '{self.model_name}' on {self.device} (compute_type={self.compute_type}, threads={self.cpu_threads})..."
        )
        t0 = time.time()
        self.model = WhisperModel(
            self.model_name,
            device=self.device,
            compute_type=self.compute_type,
            cpu_threads=self.cpu_threads
        )
        logger.info(f"Model '{self.model_name}' loaded in {time.time() - t0:.2f}s")

    def transcribe_audio_bytes(
        self,
        audio_bytes: bytes,
        sequence_id: int = 0,
        timestamp: float = 0.0,
        language: Optional[str] = None
    ) -> TranscriptionResponse:
        """
        Transcribe raw audio bytes (WebM, WAV, MP3, OGG, etc.) completely in-memory.
        Does NOT write audio to disk.
        """
        if not audio_bytes or len(audio_bytes) == 0:
            return TranscriptionResponse(
                status="empty",
                sequence_id=sequence_id,
                timestamp=timestamp,
                duration=0.0,
                language="unknown",
                language_probability=0.0,
                text="",
                segments=[],
                metrics=TranscriptionMetrics(inference_time_ms=0.0, rtf=0.0, audio_bytes=0)
            )

        bio = io.BytesIO(audio_bytes)
        lang_arg = language if (language and language.strip() and language != "auto") else None

        t0 = time.time()
        try:
            segments_gen, info = self.model.transcribe(
                bio,
                language=lang_arg,
                beam_size=1, # Fast greedy search for streaming
                word_timestamps=True,
                vad_filter=True, # Built-in Silero VAD to skip non-speech noise
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            raw_segments = list(segments_gen)
        except Exception as e:
            logger.error(f"Error during audio decoding/transcription: {e}")
            raise AudioDecodingError(f"Failed to decode audio: {str(e)}")

        inference_time_ms = (time.time() - t0) * 1000.0
        audio_duration = info.duration if info.duration > 0 else 0.01
        rtf = (inference_time_ms / 1000.0) / audio_duration

        segments: list[SegmentItem] = []
        full_text_parts: list[str] = []

        for s in raw_segments:
            seg_text = s.text.strip()
            if seg_text:
                full_text_parts.append(seg_text)

            words: list[WordItem] = []
            if s.words:
                for w in s.words:
                    words.append(WordItem(
                        word=w.word.strip(),
                        start=round(w.start, 2),
                        end=round(w.end, 2),
                        probability=round(w.probability, 2)
                    ))

            segments.append(SegmentItem(
                id=s.id,
                start=round(s.start, 2),
                end=round(s.end, 2),
                text=seg_text,
                words=words
            ))

        full_text = " ".join(full_text_parts).strip()
        status = "ok" if full_text else "empty"

        return TranscriptionResponse(
            status=status,
            sequence_id=sequence_id,
            timestamp=timestamp,
            duration=round(info.duration, 2),
            language=info.language or "en",
            language_probability=round(info.language_probability, 2) if info.language_probability else 1.0,
            text=full_text,
            segments=segments,
            metrics=TranscriptionMetrics(
                inference_time_ms=round(inference_time_ms, 1),
                rtf=round(rtf, 3),
                audio_bytes=len(audio_bytes)
            )
        )
