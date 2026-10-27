#!/usr/bin/env python3
"""usage: tl.py <project-id> -> prints line start/end (first line 0.5 s, 0.65 s gaps), the make_index VO json and total (last end + 3.4)."""
import subprocess, sys, glob
pid = sys.argv[1]; d = f"/Users/arakviel/Work/kostyl.dev/tools/hyperframes/python-core/{pid}/assets/vo"
t = 0.5; vo = []
for f in sorted(glob.glob(d + "/l*.wav"), key=lambda p: int(p.split("/l")[-1][:-4])):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
    vo.append([round(t, 2), round(dur, 2)]); print(f"l{len(vo)} {t:.2f}-{t+dur:.2f}"); t += dur + 0.65
end = vo[-1][0] + vo[-1][1]
print("claim", round(end + 0.4, 1), "total", round(end + 3.2, 1)); print(vo)
