G="/private/tmp/claude-501/-Users-arakviel-Work-kostyl-dev/82ea6f59-25c7-47d3-a3df-29a1c293aa8e/scratchpad/gen/"
K='<span style="color:#c586c0">%s</span>'
def S(x): return f'<span style="color:#ce9178">{x}</span>'
def N(x): return f'<span style="color:#b5cea8">{x}</span>'
lines=[
 '<span style="color:#569cd6">def</span> <span style="color:#dcdcaa">classify</span>(c):',
 '    '+K%'match'+' c:',
 '        '+K%'case'+' '+N(1)+':',
 '            '+K%'return'+' '+S('"один"'),
 '        '+K%'case'+' '+N(2)+' | '+N(3)+':',
 '            '+K%'return'+' '+S('"два або три"'),
 '        '+K%'case'+' '+S('"go"')+':',
 '            '+K%'return'+' '+S('"команда"'),
 '        '+K%'case'+' <span style="color:#9cdcfe">x</span> '+K%'if'+' <span style="color:#dcdcaa">isinstance</span>(<span style="color:#9cdcfe">x</span>, <span style="color:#4ec9b0">int</span>) '+K%'and'+' <span style="color:#9cdcfe">x</span> &gt; '+N(100)+':',
 '            '+K%'return'+' '+S('"велике число"'),
 '        '+K%'case'+' _:',
 '            '+K%'return'+' '+S('"інше"'),
]
code="".join(f'<div class="vsl" style="top:{118+i*54}px;font-size:30px"><span class="n" style="font-size:28px">{i+1}</span><span style="white-space:pre">{l}</span></div>' for i,l in enumerate(lines))
open(G+"y507.part","w").write('''<div id="root" data-composition-id="world" data-width="1920" data-height="1080">
  <div id="ed" class="vsw" style="left:60px;top:90px;width:1000px;height:800px">
    <div class="vsb"><span class="vsd" style="left:20px;background:#ff5f57"></span><span class="vsd" style="left:48px;background:#febc2e"></span><span class="vsd" style="left:76px;background:#28c840"></span><div class="vsT">match.py</div></div>
    <div class="vsr"></div><div class="vst">match.py</div>
''' + code + '''
    <div id="hl" style="position:absolute;left:0;width:1000px;height:54px;top:118px;background:rgba(251,191,36,0.2);opacity:0"></div>
    <div id="ok" style="position:absolute;left:0;width:1000px;height:54px;top:118px;background:rgba(52,211,153,0.25);opacity:0"></div>
  </div>
  <div id="v" class="mono abs" style="left:1120px;top:100px;font-size:52px;color:#22d3ee;opacity:0">c = 3</div>
  <div id="term" class="vsw" style="left:1120px;top:200px;width:720px;height:250px;opacity:0">
    <div class="vsb"><div class="vsT" style="text-align:left;left:24px">ТЕРМІНАЛ</div></div>
    <div id="o1" class="vsx" style="top:70px;font-size:36px">1 один</div><div id="o2" class="vsx" style="top:116px;font-size:36px;color:#34d399;font-weight:700">3 два або три</div>
    <div id="o3" class="vsx" style="top:162px;font-size:36px">go команда</div>
  </div>
  <div id="tp" class="card" style="left:1120px;top:500px;width:720px;height:420px;opacity:0">
    <div class="lab" style="left:24px;top:12px;font-size:30px;color:#fbbf24">шаблон-кортеж</div>
    <div class="mono abs" style="left:24px;top:60px;font-size:30px;color:#d4d4d4;white-space:pre">cmd = ("move", 3)
match cmd:
    case ("stop",):
        print("стоп")
    case ("move", steps):
        print("крок", steps)
    case _:
        print("?")</div>
    <div id="pt" style="position:absolute;left:12px;top:204px;width:690px;height:42px;background:rgba(52,211,153,0.25);opacity:0"></div>
    <div id="ou" class="mono abs" style="left:24px;top:350px;font-size:44px;color:#34d399;font-weight:700;opacity:0">крок 3</div>
  </div>
</div>
<script>
/*PRE*/
/*HW*/
/*T*/
const row = (k) => k * 54;
tl.set("#ed", { opacity: 1 }, 0);
tl.set("#hl", { y: row(1), opacity: 1 }, T[0] + 0.6); pulse("#ed", T[0] + 1.8, 1.01);
show("#v", T[1] + 0.2); pulse("#v", T[1] + 0.8, 1.1);
tl.set("#hl", { y: row(2) }, T[2] + 0.6); tl.set("#hl", { y: row(4) }, T[2] + 2.4);
tl.set("#hl", { opacity: 0 }, T[2] + 3.2); tl.set("#ok", { y: row(4), opacity: 1 }, T[2] + 3.2); tl.set("#ok", { y: row(5) }, T[2] + 4.0);
show("#term", T[2] + 4.2, 0.3); show("#o1", T[2] + 4.5, 0.05); show("#o2", T[2] + 4.9, 0.1); show("#o3", T[2] + 5.2, 0.05);
tl.set("#ok", { opacity: 0 }, T[3] + 0.1); tl.set("#hl", { y: row(10), opacity: 1 }, T[3] + 0.3); pulse("#ed", T[3] + 1.4, 1.01);
tl.set("#hl", { opacity: 0 }, T[4] + 0.1);
show("#tp", T[4] + 0.3, 0.3); show("#pt", T[4] + 2.6, 0.2); show("#ou", T[4] + 3.8, 0.1); pulse("#ou", T[4] + 3.9, 1.1);
hide("#v", CL - 0.35, 0.3);
window.__timelines["world"] = tl;
</script>
''')
def blk(i,left,col,title,l1,l2,l3=""):
    return f'<div id="k{i}" class="bk" style="left:{left}px;border-color:{col}"><div class="bt" style="color:{col}">{title}</div><div class="bc" style="top:96px;font-size:30px;color:#d4d4d4">{l1}</div><div class="bc" style="top:170px;font-size:56px;color:{col}">{l2}</div><div class="bc" style="top:260px;font-size:30px;color:#9fb2cf">{l3}</div></div>'
open(G+"y508.part","w").write('''<style>
.bk { position: absolute; top: 250px; width: 400px; height: 360px; border-radius: 20px; background: #0e1626; border: 4px solid #26365a; opacity: 0; }
.bt { position: absolute; left: 24px; top: 16px; font-size: 34px; font-weight: 700; }
.bc { position: absolute; left: 0; width: 400px; text-align: center; font-family: "JetBrains Mono", monospace; font-weight: 700; white-space: nowrap; }
</style>
<div id="root" data-composition-id="world" data-width="1920" data-height="1080">
  ''' + blk(1,80,"#22d3ee","порівняння","82 &gt;= 75","True") + blk(2,520,"#fbbf24","and / or","82 &gt;= 75 and 82 &lt; 90","True","зупиняється рано") + blk(3,960,"#34d399","if / elif / else","score = 82","B","одна галузь") + blk(4,1400,"#a78bfa","match",'("move", 3)',"крок 3","за шаблоном") + '''
  <div id="a1" class="ar r" style="left:480px;top:420px;width:36px;color:#9fb2cf"></div><div id="a2" class="ar r" style="left:920px;top:420px;width:36px;color:#9fb2cf"></div><div id="a3" class="ar r" style="left:1360px;top:420px;width:36px;color:#9fb2cf"></div>
</div>
<script>
/*PRE*/
/*HW*/
/*T*/
tl.set("#k1", { opacity: 1 }, 0); pulse("#k1", 0.8, 1.04);
pulse("#k1", T[1] + 0.8, 1.05);
show("#a1", T[2] + 0.1); show("#k2", T[2] + 0.3, 0.3); pulse("#k2", T[2] + 1.0, 1.05);
show("#a2", T[3] + 0.1); show("#k3", T[3] + 0.3, 0.3); pulse("#k3", T[3] + 1.0, 1.05);
show("#a3", T[4] + 0.1); show("#k4", T[4] + 0.3, 0.3); pulse("#k4", T[4] + 1.0, 1.05);
window.__timelines["world"] = tl;
</script>
''')
