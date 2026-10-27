import sys, re
ROOT = "/Users/arakviel/Work/kostyl.dev/tools/hyperframes/python-core/"
BASE = '''<style>
#root { position: absolute; inset: 0; background: #070b14; overflow: hidden; font-family: "Inter", sans-serif; color: #e8eef7; }
.mono { font-family: "JetBrains Mono", monospace; font-weight: 700; }
.abs { position: absolute; }
.card { position: absolute; border-radius: 18px; background: #0e1626; border: 3px solid #26365a; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
.lab { position: absolute; font-size: 34px; font-weight: 700; color: #9fb2cf; white-space: nowrap; }
.o0 { opacity: 0; }
.ar { position: absolute; height: 8px; background: currentColor; opacity: 0; }
.ar.r::after { content: ""; position: absolute; right: -8px; top: -14px; border-left: 28px solid currentColor; border-top: 18px solid transparent; border-bottom: 18px solid transparent; }
</style>'''
PRE = '''const tl = gsap.timeline({ paused: true });
const show = (sel, at, d = 0.3) => tl.to(sel, { opacity: 1, duration: d, ease: "power2.out" }, at);
const hide = (sel, at, d = 0.3) => tl.to(sel, { opacity: 0, duration: d, ease: "power2.in" }, at);
const pulse = (sel, at, sc = 1.1) => { tl.to(sel, { scale: sc, duration: 0.15 }, at); tl.to(sel, { scale: 1, duration: 0.3 }, at + 0.15); };'''
LINES = '''<template>
<style>
#root { position: absolute; inset: 0; font-family: "Inter", sans-serif; color: #e8eef7; }
#claim { position: absolute; left: 0; width: 1920px; top: 110px; text-align: center; font-size: 66px; font-weight: 700; letter-spacing: -0.01em; opacity: 0; }
</style>
<div id="root" data-composition-id="lines" data-width="1920" data-height="1080">
<div id="claim" class="clip" data-start="@T@" data-duration="2.6">@C@</div>
</div>
<script>
const tl = gsap.timeline({ paused: true });
tl.fromTo("#claim", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power4.out" }, @T@);
window.__timelines["lines"] = tl;
</script>
</template>
'''
pid, claim_t, claim = sys.argv[1], sys.argv[2], sys.argv[3]
part = open(f"{pid[-0:]}".replace("", "") or "").read() if False else open(sys.argv[4]).read()
part = part.replace("/*PRE*/", PRE)
open(ROOT + pid + "/compositions/world.html", "w").write("<template>\n" + BASE + "\n" + part + "\n</template>\n")
open(ROOT + pid + "/compositions/lines.html", "w").write(LINES.replace("@T@", claim_t).replace("@C@", claim))
