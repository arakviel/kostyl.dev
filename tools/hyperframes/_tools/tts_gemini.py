"""usage: tts_gemini.py <outdir> "<line 1>" "<line 2>" ...
Synthesizes Ukrainian lines with Gemini Flash TTS into <outdir>/l1.wav ...
API key is read from GEMINI_API_KEY environment variable and never written to disk.
"""
import os, sys, json, time, base64, wave, io, urllib.request, urllib.error

VOICE = os.environ.get("GEMINI_VOICE", "Puck")
KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
if not KEY:
    sys.exit("Error: GEMINI_API_KEY or GOOGLE_GENERATIVE_AI_API_KEY environment variable required")

MODELS = [
    os.environ.get("GEMINI_TTS_MODEL", "gemini-3.1-flash-tts-preview"),
    "gemini-3.8-flash-lite-tts",
    "gemini-2.5-flash-preview-tts",
]

outdir, lines = sys.argv[1], sys.argv[2:]
os.makedirs(outdir, exist_ok=True)

for i, text in enumerate(lines, 1):
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": VOICE
                    }
                }
            }
        }
    }
    data = json.dumps(payload).encode("utf-8")
    
    success = False
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={KEY}"
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req) as r:
                    res = json.loads(r.read())
                    part = res["candidates"][0]["content"]["parts"][0]["inlineData"]
                    raw_bytes = base64.b64decode(part["data"])
                    mime = part.get("mimeType", "")
                    
                    target_file = f"{outdir}/l{i}.wav"
                    if raw_bytes.startswith(b"RIFF"):
                        with open(target_file, "wb") as f:
                            f.write(raw_bytes)
                    else:
                        # Raw PCM (e.g. audio/l16; rate=24000; channels=1) -> write standard WAV
                        rate = 24000
                        if "rate=" in mime:
                            try:
                                rate = int(mime.split("rate=")[1].split(";")[0].strip())
                            except Exception:
                                pass
                        channels = 1
                        if "channels=" in mime:
                            try:
                                channels = int(mime.split("channels=")[1].split(";")[0].strip())
                            except Exception:
                                pass
                        with wave.open(target_file, "wb") as wf:
                            wf.setnchannels(channels)
                            wf.setsampwidth(2) # 16-bit
                            wf.setframerate(rate)
                            wf.writeframes(raw_bytes)
                            
                    print(f"ok {i} (line {i} with {model}, rate={rate if not raw_bytes.startswith(b'RIFF') else 'wav'})")
                    success = True
                    break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    err_msg = e.read().decode("utf-8", errors="replace")
                    if "per day limit exceeded" in err_msg or attempt == 3:
                        print(f"Model {model} quota reached, trying next model...")
                        break
                    time.sleep(5)
                else:
                    err_msg = e.read().decode("utf-8", errors="replace")
                    print(f"HTTPError on line {i}: {e.code} - {err_msg}")
                    break
            except Exception as e:
                print(f"Error on line {i}: {e}")
                time.sleep(4)
        if success:
            break
            
    if not success:
        sys.exit(f"Failed to generate line {i} across available models")
    
    time.sleep(4)
