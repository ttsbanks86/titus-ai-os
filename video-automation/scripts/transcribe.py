import whisper

model = whisper.load_model('base')
result = model.transcribe(r'C:\Users\tbank\Desktop\Hotchair\WhatsApp Video 2026-06-10 at 2.15.42 AM.mp4')

print('=== TRANSCRIPTION ===')
print(result['text'])
print()
print('=== SEGMENTS ===')
for seg in result['segments']:
    start = int(seg['start'])
    mins = start // 60
    secs = start % 60
    text = seg['text'].strip()
    print(f'[{mins:02d}:{secs:02d}] {text}')
