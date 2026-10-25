#!/usr/bin/env bash
# usage: new_video.sh <project-id> "<line 1>" "<line 2>" ...
# Creates the HyperFrames project, copies the ambient bed + SFX, synthesizes Ukrainian voice lines (StyleTTS2, voice
# "Вʼячеслав Дудко", local) and prints each line's duration and inner pauses (use them to time the scenes).
# Needs the TTS venv: TTS_PY (default: scratchpad venv built earlier with torch 2.8 + styletts2-inference, python 3.11).
set -euo pipefail
ROOT=/Users/arakviel/Work/kostyl.dev/tools/hyperframes
TTS_PY=${TTS_PY:-/private/tmp/claude-501/-Users-arakviel-Work-kostyl-dev/85ab8cd4-5d4c-4787-9d96-05cedc3cc61d/scratchpad/tts-venv/bin/python}
ID=$1; shift
N=$ROOT/cnn-image-classification/$ID
cd $ROOT/cnn-image-classification
[ -d "$N" ] || npx hyperframes init "$ID" --non-interactive 2>&1 | grep -E "✗|Created"
mkdir -p $N/assets/vo $N/assets/music $N/assets/sfx $N/compositions
cp $ROOT/_music/bed-ambient.wav $N/assets/music/bed.wav
cp $ROOT/cnn-image-classification/cv-02-rgb-channels/assets/sfx/*.mp3 $N/assets/sfx/
RAW=$(mktemp -d)
$TTS_PY $ROOT/_tools/tts_local.py "Вʼячеслав Дудко" "$RAW" "$@" 2>&1 | grep -E "Error|Traceback" || true
i=1
for _ in "$@"; do
  ffmpeg -y -loglevel error -i "$RAW/l$i.wav" -af "loudnorm=I=-16:TP=-1.5:LRA=7" -ar 44100 -ac 1 "$N/assets/vo/l$i.wav"
  echo "l$i $(ffprobe -v error -show_entries format=duration -of csv=p=0 $N/assets/vo/l$i.wav) | pauses(start dur): $(ffmpeg -i $N/assets/vo/l$i.wav -af silencedetect=noise=-32dB:d=0.1 -f null - 2>&1 | grep -E 'silence_(start|duration)' | sed 's/.*silence_//;s/duration: //;s/start: //' | paste -sd' ' -)"
  i=$((i+1))
done
rm -rf "$RAW"
