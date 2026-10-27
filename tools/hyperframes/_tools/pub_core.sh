#!/usr/bin/env bash
# usage: pub_core.sh <slot-id> <out-name> <poster-sec>   (lesson 00 of python core: renders, publishes, embeds)
set -euo pipefail
export HF_MODULE=python-core HF_VIDEO_DIR=python-core HF_IMAGE_DIR=python/core HF_IMAGE_LESSON=how-computers-run-programs HF_CONTENT_DIR=/Users/arakviel/Work/kostyl.dev/content/05.python/01.core
D=/Users/arakviel/Work/kostyl.dev/tools/hyperframes/_tools
$D/publish.sh "$1" "$2" 00-how-computers-run "$3" 2>&1 | grep -E "LUFS|published"
python3 $D/embed.py 00.how-computers-run-programs.md "$1" 00-how-computers-run "$2"
