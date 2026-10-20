import time
import os
from faster_whisper import WhisperModel

path = r'c:\AmazonMlChallenge\signbridge-backend\test_speech_sample.wav'
models = ['tiny.en', 'base.en']

for model_name in models:
    print(f"\n================ Model: {model_name} (int8, CPU) ================")
    t_load = time.time()
    model = WhisperModel(model_name, device='cpu', compute_type='int8')
    load_time = time.time() - t_load
    print(f"Model {model_name} loaded in {load_time:.2f}s")
    
    # Run warm-up and 3 runs to get an accurate average
    latencies = []
    for run in range(3):
        t0 = time.time()
        segments, info = model.transcribe(path, word_timestamps=True)
        seg_list = list(segments)
        dur = time.time() - t0
        latencies.append(dur)
        text = ' '.join(s.text.strip() for s in seg_list)
        if run == 0:
            print(f"Sample 1 Recognized: \"{text}\"")
            print(f"Audio Duration: {info.duration:.2f}s, Language: {info.language}")
    
    avg_latency = sum(latencies) / len(latencies)
    rtf = avg_latency / info.duration
    print(f"Avg Inference Latency: {avg_latency*1000:.1f}ms")
    print(f"Calculated RTF: {rtf:.3f}")
