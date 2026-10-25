#!/usr/bin/env bash
# Render one HyperFrames project and publish mp4+webm+poster into public/.
# usage: publish.sh <project-id> <out-name> <lesson-folder> <poster-seconds>
#   e.g. publish.sh pad-02-edge-stroke edge-stroke padding-and-stride 34.8
set -euo pipefail
ROOT=/Users/arakviel/Work/kostyl.dev
P=$ROOT/tools/hyperframes/cnn-image-classification/$1
OUT=$2; LESSON=$3; POSTER=$4
V=$ROOT/public/videos/ai-python/cnn-image-classification/$LESSON
I=$ROOT/public/images/ai-python/cnn-image-classification/$LESSON
mkdir -p "$V" "$I" "$P/renders"
cd "$P"
npx hyperframes render --quality delivery --output "$P/renders/$OUT.mp4" 2>&1 | grep -E "◇  /|MB|✗" || true
R="$P/renders/$OUT.mp4"
echo "$OUT: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$R")s $(ffmpeg -nostats -i "$R" -af ebur128=peak=true -f null - 2>&1 | awk '/Summary:/{p=1} p' | grep -E '^\s+I:|Peak:' | tr -s ' ' | tr '\n' ' ')"
ffmpeg -y -loglevel error -i "$R" -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart "$V/$OUT.mp4"
ffmpeg -y -loglevel error -i "$R" -c:v libvpx-vp9 -crf 33 -b:v 0 -row-mt 1 -c:a libopus -b:a 96k "$V/$OUT.webm"
ffmpeg -y -loglevel error -ss "$POSTER" -i "$R" -frames:v 1 -q:v 3 "$I/$OUT-poster.jpg"
echo "published: $V/$OUT.{mp4,webm}  $I/$OUT-poster.jpg"
