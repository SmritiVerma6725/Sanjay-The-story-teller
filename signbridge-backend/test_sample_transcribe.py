import time
from faster_whisper import WhisperModel

model = WhisperModel('tiny.en', device='cpu', compute_type='int8')
path = r'c:\AmazonMlChallenge\signbridge-backend\test_speech_sample.wav'

t0 = time.time()
segments, info = model.transcribe(path, word_timestamps=True)
seg_list = list(segments)
text = ' '.join(s.text.strip() for s in seg_list)
dur = time.time() - t0

print(f'Detected language: {info.language} ({info.language_probability:.2f}), Audio Duration: {info.duration:.2f}s')
print(f'Inference time: {dur:.3f}s, RTF: {dur/info.duration:.3f}')
print(f'Recognized text: "{text}"')
for s in seg_list:
    print(f'  Segment [{s.start:.2f}s -> {s.end:.2f}s]: "{s.text}"')
    if s.words:
        words_str = ', '.join(f"'{w.word}'({w.start:.2f}-{w.end:.2f})" for w in s.words)
        print(f'    Words: {words_str}')
