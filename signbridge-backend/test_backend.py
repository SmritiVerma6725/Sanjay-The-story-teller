import os
import io
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from main import app

SAMPLE_WAV = os.path.join(os.path.dirname(__file__), "test_speech_sample.wav")

def test_health(client):
    print("\n--- 1. Testing GET /health ---")
    response = client.get("/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    print("Health response:", data)
    assert data["status"] == "ok"
    assert data["service"] == "signbridge-backend"
    assert "model" in data
    print("  ✔ PASS: /health endpoint returned valid schema")

def test_transcribe_speech_sample(client):
    print("\n--- 2. Testing POST /api/transcribe with speech WAV sample ---")
    with open(SAMPLE_WAV, "rb") as f:
        audio_bytes = f.read()

    files = {"audio": ("sample.wav", audio_bytes, "audio/wav")}
    data = {"sequence_id": 1, "timestamp": 0.0, "language": "en"}

    t0 = time.time()
    response = client.post("/api/transcribe", files=files, data=data)
    dur = time.time() - t0
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    res = response.json()
    print(f"Transcription response ({dur:.2f}s):", res["text"])
    print("Metrics:", res["metrics"])
    assert res["status"] == "ok"
    assert "sign" in res["text"].lower() or "bridge" in res["text"].lower()
    assert len(res["segments"]) > 0
    print("  ✔ PASS: /api/transcribe returned accurate speech transcription and word segments")

def test_transcribe_sliced_speech_sample(client):
    print("\n--- 3. Testing POST /api/transcribe with 2.0s sequential slices ---")
    import wave
    with wave.open(SAMPLE_WAV, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        total_frames = wf.getnframes()
        all_frames = wf.readframes(total_frames)

    frames_per_slice = int(framerate * 2.0)
    bytes_per_frame = n_channels * sampwidth
    bytes_per_slice = frames_per_slice * bytes_per_frame

    sequence_responses = []
    num_slices = (len(all_frames) + bytes_per_slice - 1) // bytes_per_slice

    for seq in range(1, num_slices + 1):
        start_byte = (seq - 1) * bytes_per_slice
        end_byte = min(seq * bytes_per_slice, len(all_frames))
        slice_data = all_frames[start_byte:end_byte]
        slice_frames = len(slice_data) // bytes_per_frame
        slice_timestamp = (seq - 1) * 2.0

        bio = io.BytesIO()
        with wave.open(bio, "wb") as slice_wf:
            slice_wf.setnchannels(n_channels)
            slice_wf.setsampwidth(sampwidth)
            slice_wf.setframerate(framerate)
            slice_wf.writeframes(slice_data)
        bio.seek(0)

        files = {"audio": (f"chunk_{seq}.wav", bio.read(), "audio/wav")}
        data = {"sequence_id": seq, "timestamp": slice_timestamp, "language": "en"}

        t0 = time.time()
        resp = client.post("/api/transcribe", files=files, data=data)
        dur = time.time() - t0

        assert resp.status_code == 200, f"Chunk {seq} failed: {resp.text}"
        res = resp.json()
        print(f"  Chunk #{seq} (t={slice_timestamp:.1f}s, len={slice_frames/framerate:.2f}s, inf={dur:.2f}s): text='{res['text']}', rtf={res['metrics']['rtf']}")
        assert res["sequence_id"] == seq, f"Sequence ID mismatch: {res['sequence_id']} != {seq}"
        assert abs(res["timestamp"] - slice_timestamp) < 0.01, f"Timestamp mismatch: {res['timestamp']} != {slice_timestamp}"
        sequence_responses.append(res)

    print(f"  ✔ PASS: Successfully processed {len(sequence_responses)} sequential audio slices with intact order and metadata")

def test_transcribe_empty_file(client):
    print("\n--- 4. Testing POST /api/transcribe with empty file ---")
    files = {"audio": ("empty.wav", b"", "audio/wav")}
    response = client.post("/api/transcribe", files=files, data={"sequence_id": 10})
    assert response.status_code == 200
    res = response.json()
    assert res["status"] == "empty"
    assert res["text"] == ""
    print("  ✔ PASS: empty audio handled gracefully with status='empty'")

def test_transcribe_corrupted_file(client):
    print("\n--- 5. Testing POST /api/transcribe with corrupted audio bytes ---")
    files = {"audio": ("corrupted.wav", b"NOT_A_VALID_AUDIO_FILE_DATA_1234567890", "audio/wav")}
    response = client.post("/api/transcribe", files=files, data={"sequence_id": 11})
    assert response.status_code == 400
    print("  ✔ PASS: corrupted audio returned HTTP 400 Bad Request")

def test_transcribe_oversized_file(client):
    print("\n--- 6. Testing POST /api/transcribe with oversized payload (> 10MB) ---")
    large_data = b"0" * (11 * 1024 * 1024)
    files = {"audio": ("large.wav", large_data, "audio/wav")}
    response = client.post("/api/transcribe", files=files, data={"sequence_id": 12})
    assert response.status_code == 413
    print("  ✔ PASS: oversized audio returned HTTP 413 Payload Too Large")

def test_offline_privacy(client):
    print("\n--- 7. Testing Privacy Boundary: No external audio transmission ---")
    import socket
    original_connect = socket.socket.connect
    external_calls = []

    def mock_connect(self, address):
        host, port = address[0], address[1]
        # Only local loopback connections are permitted
        if str(host) not in ("127.0.0.1", "localhost", "::1", "testserver"):
            external_calls.append((host, port))
            raise RuntimeError(f"Prohibited external network call detected to {host}:{port}")
        return original_connect(self, address)

    # Monkey-patch socket.connect during test
    socket.socket.connect = mock_connect
    try:
        with open(SAMPLE_WAV, "rb") as f:
            audio_bytes = f.read()
        files = {"audio": ("sample.wav", audio_bytes, "audio/wav")}
        data = {"sequence_id": 99, "timestamp": 0.0, "language": "en"}
        response = client.post("/api/transcribe", files=files, data=data)
        assert response.status_code == 200
        assert len(external_calls) == 0, f"External network calls made: {external_calls}"
        print("  ✔ PASS: Zero external network calls made during transcription (strictly local)")
    finally:
        socket.socket.connect = original_connect

def test_latest_transcript(client):
    print("\n--- 8. Testing GET /api/transcript/latest ---")
    response = client.get("/api/transcript/latest")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["sequence_id"] == 99
    print(f"  Latest transcript: sequence_id={data['sequence_id']}, text='{data['text']}'")
    print("  ✔ PASS: /api/transcript/latest returned most recent transcription result")

def run_all():
    with TestClient(app) as client:
        test_health(client)
        test_transcribe_speech_sample(client)
        test_transcribe_sliced_speech_sample(client)
        test_transcribe_empty_file(client)
        test_transcribe_corrupted_file(client)
        test_transcribe_oversized_file(client)
        test_offline_privacy(client)
        test_latest_transcript(client)
        print("\n==========================================")
        print("All 8 Backend Unit & Integration Tests PASSED!")
        print("==========================================")

if __name__ == "__main__":
    run_all()

