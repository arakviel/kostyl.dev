G="/private/tmp/claude-501/-Users-arakviel-Work-kostyl-dev/82ea6f59-25c7-47d3-a3df-29a1c293aa8e/scratchpad/gen/"
V='<div class="vsb"><span class="vsd" style="left:20px;background:#ff5f57"></span><span class="vsd" style="left:48px;background:#febc2e"></span><span class="vsd" style="left:76px;background:#28c840"></span><div class="vsT">%s</div></div><div class="vsr"></div><div class="vst">%s</div>'
wall="".join(f'<div class="vsl" style="top:{118+k*54}px;font-size:32px"><span class="n" style="font-size:28px">{k+1}</span><span style="white-space:pre"><span style="color:#dcdcaa">print</span>(<span style="color:#b5cea8">{k+1}</span>)</span></div>' for k in range(10))
open(G+"z601.part","w").write('''<div id="root" data-composition-id="world" data-width="1920" data-height="1080">
  <div id="w" class="vsw" style="left:80px;top:100px;width:760px;height:800px">''' + V%("wall.py","wall.py") + '''
    <div id="wl" class="abs" style="left:0;top:0;width:760px;height:800px">''' + wall + '''<div class="vsl" style="top:658px;font-size:32px;color:#6f84a6"><span class="n" style="font-size:28px">⋮</span></div><div class="vsl" style="top:712px;font-size:32px"><span class="n" style="font-size:28px">1000</span><span style="white-space:pre"><span style="color:#dcdcaa">print</span>(<span style="color:#b5cea8">1000</span>)</span></div></div>
  </div>
  <div id="x1" class="abs" style="left:100px;top:490px;width:720px;height:16px;background:#fb7185;border-radius:8px;transform:rotate(36deg);opacity:0"></div>
  <div id="x2" class="abs" style="left:100px;top:490px;width:720px;height:16px;background:#fb7185;border-radius:8px;transform:rotate(-36deg);opacity:0"></div>
  <div id="cnt" class="mono abs" style="left:80px;top:920px;width:760px;text-align:center;font-size:44px;color:#fb7185;opacity:0">1000 рядків</div>
  <div id="lp" class="vsw" style="left:1000px;top:200px;width:820px;height:300px;opacity:0">''' + V%("loop.py","loop.py") + '''
    <div class="vsl" style="top:118px"><span class="n">1</span><span style="white-space:pre"><span style="color:#c586c0">for</span> <span style="color:#9cdcfe">i</span> <span style="color:#c586c0">in</span> <span style="color:#dcdcaa">range</span>(<span style="color:#b5cea8">1</span>, <span style="color:#b5cea8">1001</span>):</span></div>
    <div class="vsl" style="top:172px"><span class="n">2</span><span style="white-space:pre">    <span style="color:#dcdcaa">print</span>(<span style="color:#9cdcfe">i</span>)</span></div>
  </div>
  <div id="rl" class="lab" style="left:1000px;top:540px;font-size:42px;color:#34d399;opacity:0">правило повторення</div>
  <div id="term" class="vsw" style="left:1000px;top:620px;width:820px;height:380px;opacity:0">
    <div class="vsb"><div class="vsT" style="text-align:left;left:24px">ТЕРМІНАЛ</div></div>
    <div id="o1" class="vsx" style="top:64px;font-size:36px">1</div><div id="o2" class="vsx" style="top:110px;font-size:36px">2</div><div id="o3" class="vsx" style="top:156px;font-size:36px">3</div>
    <div id="o4" class="vsx" style="top:202px;font-size:36px;color:#6f84a6">…</div><div id="o5" class="vsx" style="top:248px;font-size:36px;color:#34d399;font-weight:700">1000</div>
  </div>
</div>
<script>
/*PRE*/
/*HW*/
/*T*/
tl.set("#w", { opacity: 1 }, 0);
for (let k = 0; k < 12; k++) tl.fromTo("#wl > div:nth-of-type(" + (k + 1) + ")", { opacity: 0 }, { opacity: 1, duration: 0.1 }, 0.1 + k * 0.28);
show("#cnt", T[0] + 1.6); show("#x1", T[0] + 2.8, 0.2); show("#x2", T[0] + 3.1, 0.2);
hide("#w", T[1] + 0.1, 0.3); hide("#x1", T[1] + 0.1, 0.3); hide("#x2", T[1] + 0.1, 0.3); hide("#cnt", T[1] + 0.1, 0.3);
show("#lp", T[1] + 0.5, 0.3); show("#rl", T[1] + 2.0); pulse("#lp", T[1] + 2.4, 1.02);
show("#term", T[2] + 0.3, 0.3); ["#o1", "#o2", "#o3", "#o4", "#o5"].forEach((s, i) => show(s, T[2] + 0.8 + i * 0.5, 0.1));
pulse("#o5", T[2] + 3.4, 1.1); pulse("#lp", T[2] + 3.8, 1.02);
hide("#lp", CL - 0.35, 0.3); hide("#rl", CL - 0.35, 0.3);
window.__timelines["world"] = tl;
</script>
''')
