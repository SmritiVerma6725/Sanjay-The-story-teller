import os
from pydantic import BaseModel

class Settings(BaseModel):
    host: str = os.getenv("SIGNBRIDGE_HOST", "127.0.0.1")
    port: int = int(os.getenv("SIGNBRIDGE_PORT", "8765"))
    model_name: str = os.getenv("SIGNBRIDGE_MODEL", "tiny.en")
    compute_type: str = os.getenv("SIGNBRIDGE_COMPUTE_TYPE", "int8")
    device: str = os.getenv("SIGNBRIDGE_DEVICE", "cpu")
    cpu_threads: int = int(os.getenv("SIGNBRIDGE_CPU_THREADS", "4"))
    max_audio_bytes: int = int(os.getenv("SIGNBRIDGE_MAX_AUDIO_BYTES", str(10 * 1024 * 1024))) # 10 MB limit
    default_language: str = os.getenv("SIGNBRIDGE_DEFAULT_LANGUAGE", "en") # 'en' or empty for auto-detect

settings = Settings()
