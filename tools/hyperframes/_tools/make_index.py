#!/usr/bin/env python3
"""usage: make_index.py <project-id> <duration-s> '<vo json: [[start, dur], ...]>' '<sfx json: [[name, start, dur], ...]>'
Writes index.html for a project: world + lines scenes, ambient bed (one element, fades), VO l1..ln, SFX."""
import json, sys
pid, dur, vo, sfx = sys.argv[1], float(sys.argv[2]), json.loads(sys.argv[3]), json.loads(sys.argv[4])
a = "".join(f'      <audio id="vo{i+1}" src="assets/vo/l{i+1}.wav" data-start="{s}" data-duration="{d}" data-track-index="4" data-volume="1"></audio>\n' for i, (s, d) in enumerate(vo))
a += "".join(f'      <audio id="sfx{i+1}" src="assets/sfx/{n}.mp3" data-start="{s}" data-duration="{d}" data-track-index="5" data-volume="0.5"></audio>\n' for i, (n, s, d) in enumerate(sfx))
html = f'''<!doctype html>
<html lang="uk">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #070b14; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
      <div id="world" data-composition-id="world" data-composition-src="compositions/world.html"
           data-start="0" data-duration="{dur}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="lines" data-composition-id="lines" data-composition-src="compositions/lines.html"
           data-start="0" data-duration="{dur}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <audio id="music" src="assets/music/bed.wav" data-start="0" data-duration="{dur}" data-track-index="3" data-volume="0.16" data-fade-in="1.5" data-fade-out="2" data-timeline-role="music"></audio>
{a}    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open(f"/Users/arakviel/Work/kostyl.dev/tools/hyperframes/cnn-image-classification/{pid}/index.html", "w").write(html)
print("index.html written for", pid)
