"""Download official Apache-2.0 MediaPipe Task models for local offline motion extraction."""
import urllib.request
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MODELS = {
    "holistic_landmarker.task": "https://storage.googleapis.com/mediapipe-models/holistic_landmarker/holistic_landmarker/float16/latest/holistic_landmarker.task",
    "pose_landmarker.task": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task",
    "hand_landmarker.task": "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
}

def main():
    print("Downloading MediaPipe offline model assets...")
    for filename, url in MODELS.items():
        dest = MODELS_DIR / filename
        if dest.exists() and dest.stat().st_size > 0:
            print(f"Already exists: {filename} ({dest.stat().st_size} bytes)")
            continue
        print(f"Fetching {filename} from {url}...")
        urllib.request.urlretrieve(url, dest)
        print(f"Downloaded: {filename} ({dest.stat().st_size} bytes)")
    print("All models ready for offline processing.")

if __name__ == "__main__":
    main()
