#!/usr/bin/env bash
# usage: new_video_gemini.sh <module> <project-id> "<line 1>" "<line 2>" ...   (needs GEMINI_API_KEY in the environment)
set -euo pipefail
ROOT=/Users/arakviel/Work/kostyl.dev/tools/hyperframes
MOD=$1; ID=$2; shift 2
N=$ROOT/$MOD/$ID
mkdir -p "$ROOT/$MOD"; cd "$ROOT/$MOD"
[ -d "$N" ] || npx hyperframes init "$ID" --non-interactive 2>&1 | grep -E "✗|Created"
mkdir -p "$N/assets/vo" "$N/assets/music" "$N/assets/sfx" "$N/compositions"
cp "$ROOT/_music/bed-ambient.wav" "$N/assets/music/bed.wav"
cp "$ROOT/cnn-image-classification/cv-02-rgb-channels/assets/sfx/"*.mp3 "$N/assets/sfx/"
RAW=$(mktemp -d)
python3 -I "$ROOT/_tools/tts_gemini.py" "$RAW" "$@"
i=1
for _ in "$@"; do
  ffmpeg -y -loglevel error -i "$RAW/l$i.wav" -af "loudnorm=I=-16:TP=-1.5:LRA=7" -ar 44100 -ac 1 "$N/assets/vo/l$i.wav"
  echo "l$i $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$N/assets/vo/l$i.wav") | pauses(start dur): $(ffmpeg -i "$N/assets/vo/l$i.wav" -af silencedetect=noise=-32dB:d=0.1 -f null - 2>&1 | grep -E 'silence_(start|duration)' | sed 's/.*silence_//;s/duration: //;s/start: //' | paste -sd' ' -)"
  i=$((i+1))
done
rm -rf "$RAW"

