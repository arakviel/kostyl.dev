code_lines = [
 '<span style="color:#dcdcaa">print</span><span style="color:#ffd700">(</span><span style="color:#b5cea8">2 + 3</span><span style="color:#ffd700">)</span>',
 '<span style="color:#dcdcaa">print</span><span style="color:#ffd700">(</span><span style="color:#ce9178">"Hello"</span><span style="color:#ffd700">)</span>',
 '<span style="color:#dcdcaa">print</span><span style="color:#ffd700">(</span><span style="color:#ce9178">"Готово"</span><span style="color:#ffd700">)</span>',
]
def editor(pfx, left, top, color):
    rows = "".join(f'<div class="vsl" style="top:{112 + k * 58}px"><span class="n">{k + 1}</span>{code_lines[k]}</div>' for k in range(3))
    return f'''<div id="{pfx}ed" class="vsw" style="left:{left}px;top:{top}px;width:760px;height:340px">
  <div class="vsb"><span class="vsd" style="left:20px;background:#ff5f57"></span><span class="vsd" style="left:48px;background:#febc2e"></span><span class="vsd" style="left:76px;background:#28c840"></span><div class="vsT">program</div></div>
  <div class="vsr"></div><div class="vst">program</div>
  <div id="{pfx}bar" style="position:absolute;left:0;width:760px;height:54px;top:112px;background:{color};opacity:0"></div>
  {rows}
</div>'''
def term(pfx, cmd, outs, left=1280, top=640):
    o = "".join(f'<div id="{pfx}o{k}" class="vsx" style="top:{104 + k * 52}px">{t}</div>' for k, t in enumerate(outs))
    return f'''<div id="{pfx}term" class="vsw" style="left:{left}px;top:{top}px;width:570px;height:330px">
  <div class="vsb"><div class="vsT" style="text-align:left;left:24px">ТЕРМІНАЛ</div></div>
  <div id="{pfx}c" class="vsx" style="top:52px"><span id="{pfx}cy" class="ty">{cmd}</span></div>{o}</div>'''
html = f'''<style>
.bxx {{ position: absolute; border-radius: 16px; background: #0e1626; border: 4px solid #26365a; display: flex; align-items: center; justify-content: center; font-size: 38px; font-weight: 700; opacity: 0; }}
.pill {{ position: absolute; top: 150px; height: 70px; border-radius: 35px; border: 4px solid #26365a; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: 700; color: #9fb2cf; opacity: 0; }}
.hxr {{ position: absolute; left: 30px; font-family: "JetBrains Mono", monospace; font-weight: 700; font-size: 32px; overflow: hidden; width: 0; white-space: nowrap; }}
</style>
<div id="root" data-composition-id="world" data-width="1920" data-height="1080">
  <div id="pl1" class="pill" style="left:470px;width:400px">компілятор</div>
  <div id="pl2" class="pill" style="left:960px;width:440px">інтерпретатор</div>
  <div id="cs" style="opacity:0">
    {editor("c", 70, 260, "rgba(34,211,238,0.2)")}
    <div id="cbx" class="bxx" style="left:900px;top:335px;width:300px;height:130px;border-color:#22d3ee;color:#22d3ee">компілятор</div>
    <div id="car1" class="ar r" style="left:835px;top:396px;width:55px;color:#22d3ee"></div>
    <div id="car2" class="ar r" style="left:1210px;top:396px;width:60px;color:#fbbf24"></div>
    <div id="cexe" class="card" style="left:1280px;top:260px;width:570px;height:340px;border-color:#fbbf24;opacity:0">
      <div class="lab" style="left:28px;top:18px;font-size:30px;color:#fbbf24">нулі й одиниці (схематично)</div>
      <div id="ch0" class="hxr" style="top:100px;color:#fbbf24">10111000 00000101 11101000</div>
      <div id="ch1" class="hxr" style="top:170px;color:#fbbf24">01001000 10001101 00111101</div>
      <div id="ch2" class="hxr" style="top:240px;color:#fbbf24">01001000 10001101 00110101</div>
    </div>
    <div id="cnote" class="lab" style="left:70px;top:625px;color:#fb7185;opacity:0;font-size:34px">вихідний текст більше не потрібен</div>
    {term("c", "$ ./program", ["5", "Hello", "Готово"])}
  </div>
  <div id="is" style="opacity:0">
    {editor("i", 70, 260, "rgba(52,211,153,0.22)")}
    <div id="ibx" class="bxx" style="left:900px;top:335px;width:300px;height:130px;border-color:#34d399;color:#34d399">інтерпретатор</div>
    <div id="iar1" class="ar r" style="left:835px;top:396px;width:55px;color:#34d399"></div>
    <div id="iar2" class="ar r" style="left:1210px;top:396px;width:60px;color:#fbbf24"></div>
    <div id="icard" class="card" style="left:1280px;top:260px;width:570px;height:340px;border-color:#fbbf24">
      <div class="lab" style="left:28px;top:18px;font-size:30px;color:#fbbf24">нулі й одиниці (схематично)</div>
      <div id="ih0" class="hxr" style="top:150px;color:#fbbf24">10111000 00000101 11101000</div>
      <div id="ih1" class="hxr" style="top:150px;color:#fbbf24">01001000 10001101 00111101</div>
      <div id="ih2" class="hxr" style="top:150px;color:#fbbf24">01001000 10001101 00110101</div>
    </div>
    <div id="inote" class="lab" style="left:70px;top:625px;color:#34d399;opacity:0;font-size:34px">щоразу під час запуску</div>
    {term("i", "$ interpreter program", ["5", "Hello", "Готово"])}
  </div>
  <div id="cpu" class="card" style="left:900px;top:560px;width:300px;height:130px;border-color:#22d3ee;opacity:0"><div class="mono abs" style="left:0;width:300px;top:34px;text-align:center;font-size:56px;color:#22d3ee">CPU</div></div>
  <div id="cmdl" class="lab" style="left:900px;top:710px;width:300px;text-align:center;color:#e8eef7;opacity:0">команди</div>
</div>
'''
open("v06b.part", "w").write(html + open("v06b.js").read())
