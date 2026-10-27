"""usage: tts_cartesia.py <outdir> "<line 1>" "<line 2>" ...
Synthesizes Ukrainian lines with Cartesia (voice "Oleh - Professional Guy") into <outdir>/l1.wav ...
The key is read from CARTESIA_API_KEY and never written to disk."""
import os, sys, json, urllib.request
VOICE = os.environ.get("CARTESIA_VOICE", "05ffab9c-d380-4909-8375-cd12f59238c3")
SPEED = float(os.environ.get("CARTESIA_SPEED", "1.0"))
outdir, lines = sys.argv[1], sys.argv[2:]
for i, text in enumerate(lines, 1):
    body = {
        "model_id": "sonic-3", "transcript": text, "language": "uk",
        "voice": {"mode": "id", "id": VOICE},
        "generation_config": {"speed": SPEED},
        "output_format": {"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
    }
    req = urllib.request.Request("https://api.cartesia.ai/tts/bytes", json.dumps(body).encode(), {
        "X-API-Key": os.environ["CARTESIA_API_KEY"], "Cartesia-Version": "2025-04-16", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r, open(f"{outdir}/l{i}.wav", "wb") as f:
        f.write(r.read())
    print("ok", i)
