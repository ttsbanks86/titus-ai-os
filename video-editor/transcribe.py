import whisper, json
model = whisper.load_model('tiny')
result = model.transcribe(r'C:\Users\tbank\Desktop\Live Cowork\video-editor\narration.wav')
segments = [{'text': seg['text'].strip(), 'start': round(seg['start'], 2), 'end': round(seg['end'], 2)} for seg in result['segments']]
with open(r'C:\Users\tbank\Desktop\Live Cowork\video-editor\transcript.json', 'w') as f:
    json.dump(segments, f, indent=2)
print(f'Transcription complete: {len(segments)} segments')
for s in segments:
    print(f"  [{s['start']:.1f}s - {s['end']:.1f}s] {s['text']}")