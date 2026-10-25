#!/usr/bin/env python3
"""usage: embed.py <lesson-file.md> <slot-id> <lesson-folder> <out-name>
Replaces the `<!-- VIDEO id: <slot-id> ... -->` comment with a <video controls> block (mp4 + webm + poster)."""
import sys
md, slot, folder, name = sys.argv[1:5]
p = f"/Users/arakviel/Work/kostyl.dev/content/16.ai-python/15.cnn-image-classification/{md}"
s = open(p).read()
a = s.index(f"<!-- VIDEO\nid: {slot}"); b = s.index("-->", a) + 3
base_v = f"/videos/ai-python/cnn-image-classification/{folder}/{name}"
poster = f"/images/ai-python/cnn-image-classification/{folder}/{name}-poster.jpg"
vid = f'''<video controls preload="metadata" playsinline poster="{poster}" class="diagram-img rounded-xl shadow-lg w-full my-6">
  <source src="{base_v}.mp4" type="video/mp4">
  <source src="{base_v}.webm" type="video/webm">
</video>'''
open(p, "w").write(s[:a] + vid + s[b:])
print("embedded", slot, "->", md)
