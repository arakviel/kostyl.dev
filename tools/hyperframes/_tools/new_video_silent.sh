#!/usr/bin/env bash
# usage: new_video_silent.sh <module> <project-id> <dur1> <dur2> ...   (no voice-over: music bed + silent line tracks for timing)
set -euo pipefail
ROOT=/Users/arakviel/Work/kostyl.dev/tools/hyperframes
MOD=$1; ID=$2; shift 2
N=$ROOT/$MOD/$ID
mkdir -p $ROOT/$MOD; cd $ROOT/$MOD
[ -f "$N/hyperframes.json" ] || npx hyperframes init "$ID" --non-interactive 2>&1 | grep -E "✗|Created"
mkdir -p $N/assets/vo $N/assets/music $N/assets/sfx $N/compositions
cp $ROOT/_music/bed-ambient.wav $N/assets/music/bed.wav
i=1
for d in "$@"; do ffmpeg -y -loglevel error -f lavfi -i anullsrc=r=44100:cl=mono -t "$d" "$N/assets/vo/l$i.wav"; i=$((i+1)); done
echo "silent project $ID: $# lines"
