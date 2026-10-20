import sys
import uvicorn
from config import settings

def start_server():
    print(f"Starting SignBridge Speech Recognition Service on http://{settings.host}:{settings.port}")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level="info",
        access_log=False # Avoid logging every chunk GET/POST to keep logs concise
    )

if __name__ == "__main__":
    start_server()
