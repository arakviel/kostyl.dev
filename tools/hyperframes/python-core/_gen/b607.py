G="/private/tmp/claude-501/-Users-arakviel-Work-kostyl-dev/82ea6f59-25c7-47d3-a3df-29a1c293aa8e/scratchpad/gen/"
CAPCSS='.cpt { position: absolute; left: 80px; width: 1760px; top: 975px; text-align: center; font-size: 40px; font-weight: 700; color: #fbbf24; opacity: 0; }'
CAPJS='''const $ = (id) => document.getElementById(id);
CAPS.forEach((t, i) => { $("caps").insertAdjacentHTML("beforeend", `<div id="cp${i}" class="cpt">${t}</div>`); show("#cp" + i, T[i] + 0.2, 0.3); hide("#cp" + i, (i < CAPS.length - 1 ? T[i + 1] - 0.15 : CL - 0.35), 0.25); });'''
V='<div class="vsb"><span class="vsd" style="left:20px;background:#ff5f57"></span><span class="vsd" style="left:48px;background:#febc2e"></span><span class="vsd" style="left:76px;background:#28c840"></span><div class="vsT">%s</div></div><div class="vsr"></div><div class="vst">%s</div>'
K='<span style="color:#c586c0">%s</span>'
def N(x): return f'<span style="color:#b5cea8">{x}</span>'
def L(k,n,html,fs=36): return f'<div class="vsl" style="top:{118+k*54}px;font-size:{fs}px"><span class="n">{n}</span><span style="white-space:pre">{html}</span></div>'
code=[K%'for'+' <span style="color:#9cdcfe">i</span> '+K%'in'+' <span style="color:#dcdcaa">range</span>('+N(1)+', '+N(4)+'):', '    '+K%'for'+' <span style="color:#9cdcfe">j</span> '+K%'in'+' <span style="color:#dcdcaa">range</span>('+N(1)+', '+N(4)+'):', '        <span style="color:#dcdcaa">print</span>(<span style="color:#9cdcfe">i</span> * <span style="color:#9cdcfe">j</span>, <span style="color:#9cdcfe">end</span>=<span style="color:#ce9178">"\\t"</span>)', '    <span style="color:#dcdcaa">print</span>()']
c="".join(L(i,i+1,l) for i,l in enumerate(code))
cells="".join(f'<div id="c{i}{j}" class="cell7" style="left:{190+(j-1)*200}px;top:{600+(i-1)*125}px"><span id="v{i}{j}" style="opacity:0">{i*j}</span></div>' for i in (1,2,3) for j in (1,2,3))
heads="".join(f'<div class="hd7" style="left:{190+(j-1)*200}px;top:545px">j={j}</div>' for j in (1,2,3))+"".join(f'<div class="hd7" style="left:60px;top:{628+(i-1)*125}px;width:110px;text-align:right">i={i}</div>' for i in (1,2,3))
ticks="".join(f'<div class="abs" style="left:{1500-4}px;top:{410-215}px;width:8px;height:28px;background:#5a6c8c;transform-origin:4px 215px;transform:rotate({a}deg)"></div>' for a in range(0,360,30))
open(G+"z607.part","w").write(f'''<style>
{CAPCSS}
.cell7 {{ position: absolute; width: 180px; height: 110px; border-radius: 14px; background: #0e1626; border: 4px solid #26365a; display: flex; align-items: center; justify-content: center; font-family: "JetBrains Mono", monospace; font-weight: 800; font-size: 60px; color: #34d399; }}
.hd7 {{ position: absolute; width: 180px; text-align: center; font-family: "JetBrains Mono", monospace; font-size: 32px; color: #9fb2cf; }}
.hand {{ position: absolute; left: 1493px; border-radius: 7px; transform-origin: 7px 100%; }}
</style>
<div id="root" data-composition-id="world" data-width="1920" data-height="1080">
  <div id="ed" class="vsw" style="left:60px;top:100px;width:900px;height:380px">{V%("nested.py","nested.py")}{c}
    <div id="hl" style="position:absolute;left:0;width:900px;height:54px;top:118px;background:rgba(251,191,36,0.2);opacity:0"></div></div>
  {heads}{cells}
  <div class="abs" style="left:1280px;top:190px;width:440px;height:440px;border-radius:220px;border:6px solid #3a4a6e;background:#0e1626"></div>
  {ticks}
  <div id="hi" class="hand" style="top:{410-120}px;width:14px;height:120px;background:#34d399"></div>
  <div id="hj" class="hand" style="top:{410-190}px;width:8px;height:190px;background:#22d3ee;left:1496px;transform-origin:4px 100%"></div>
  <div class="abs" style="left:1486px;top:396px;width:28px;height:28px;border-radius:14px;background:#e8eef7"></div>
  <div class="lab" style="left:1240px;top:690px;font-size:34px;color:#34d399">коротка стрілка — зовнішній i</div>
  <div class="lab" style="left:1240px;top:740px;font-size:34px;color:#22d3ee">довга стрілка — внутрішній j</div>
  <div class="lab" style="left:1240px;top:800px;font-size:28px;color:#6f84a6">схема: стрілки показують стан циклів</div>
  <div id="n9" class="mono abs" style="left:1240px;top:850px;width:560px;text-align:center;font-size:60px;color:#fbbf24;opacity:0">9 ітерацій</div>
  <div id="caps"></div>
</div>
<script>
/*PRE*/
/*HW*/
/*T*/
const CAPS = ["Вкладені цикли працюють як годинник", "зовнішній цикл робить один крок, внутрішній проходить усе своє коло", "i = 1: j пробігає 1, 2, 3 → рядок 1 2 3", "i = 2 і i = 3: внутрішній цикл щоразу починається заново", "3 × 3 = 9 ітерацій"];
{CAPJS}
const row = (k) => k * 54;
const ang = (v) => (v - 1) * 120;
tl.set("#ed", {{ opacity: 1 }}, 0);
tl.set("#hi", {{ rotation: 0 }}, 0); tl.set("#hj", {{ rotation: 0 }}, 0);
const cur = (i, j, at) => {{ tl.to("#c" + i + j, {{ borderColor: "#fbbf24", duration: 0.2 }}, at); tl.to("#v" + i + j, {{ opacity: 1, duration: 0.2 }}, at + 0.1); tl.to("#hj", {{ rotation: ang(j), duration: 0.4 }}, at - 0.1); tl.to("#c" + i + j, {{ borderColor: "#34d399", duration: 0.3 }}, at + 0.7); pulse("#c" + i + j, at + 0.1, 1.08); }};
// L1 clock
pulse("#ed", T[0] + 0.8, 1.02); tl.set("#hl", {{ y: row(0), opacity: 1 }}, T[0] + 1.2); tl.set("#hl", {{ y: row(1) }}, T[0] + 2.4);
// L2 one outer step, full inner circle
tl.to("#hi", {{ rotation: ang(1), duration: 0.4 }}, T[1] + 0.4);
tl.to("#hj", {{ rotation: 360, duration: 3.0, ease: "power1.inOut" }}, T[1] + 1.2); tl.set("#hj", {{ rotation: 0 }}, T[1] + 4.4);
// L3 i = 1
tl.set("#hl", {{ y: row(2) }}, T[2] + 0.4);
cur(1, 1, T[2] + 0.8); cur(1, 2, T[2] + 2.0); cur(1, 3, T[2] + 3.2); tl.set("#hl", {{ y: row(3) }}, T[2] + 4.6);
// L4 i = 2 and i = 3
tl.set("#hl", {{ y: row(0) }}, T[3] + 0.2); tl.to("#hi", {{ rotation: ang(2), duration: 0.4 }}, T[3] + 0.3);
tl.set("#hl", {{ y: row(2) }}, T[3] + 0.8);
cur(2, 1, T[3] + 0.9); cur(2, 2, T[3] + 1.5); cur(2, 3, T[3] + 2.1);
tl.set("#hl", {{ y: row(0) }}, T[3] + 2.9); tl.to("#hi", {{ rotation: ang(3), duration: 0.4 }}, T[3] + 3.0); tl.set("#hl", {{ y: row(2) }}, T[3] + 3.4);
cur(3, 1, T[3] + 3.5); cur(3, 2, T[3] + 4.1); cur(3, 3, T[3] + 4.7);
// L5 nine iterations
tl.set("#hl", {{ opacity: 0 }}, T[4] + 0.1); show("#n9", T[4] + 0.6, 0.3); pulse("#n9", T[4] + 1.2, 1.08);
for (const i of [1, 2, 3]) for (const j of [1, 2, 3]) pulse("#c" + i + j, T[4] + 1.0 + ((i - 1) * 3 + j - 1) * 0.2, 1.05);
hide("#n9", CL - 0.35, 0.2); hide("#ed", CL - 0.35, 0.3);
window.__timelines["world"] = tl;
</script>
''')
def blk(i,left,col,title,l1,big,sub):
    return f'<div id="k{i}" class="bk" style="left:{left}px;border-color:{col}"><div class="bt" style="color:{col}">{title}</div><div class="bc" style="top:100px;font-size:30px;color:#d4d4d4">{l1}</div><div class="bc" style="top:180px;font-size:58px;color:{col}">{big}</div><div class="bc" style="top:290px;font-size:30px;color:#9fb2cf;font-family:Inter,sans-serif">{sub}</div></div>'
B1=blk(1,60,"#22d3ee","while","n &gt; 0","total = 6","поки умова істинна")
B2=blk(2,520,"#34d399","for",'ch in &quot;кіт&quot;',"к і т","ітератор бере по одному")
B3=blk(3,980,"#fbbf24","range","range(10**12)","48 байтів","лише обчислює числа")
B4=blk(4,1440,"#a78bfa","break / continue / else","17 → дільника немає","просте","керують ходом циклу")
open(G+"z608.part","w").write(f'''<style>
{CAPCSS}
.bk {{ position: absolute; top: 250px; width: 420px; height: 400px; border-radius: 20px; background: #0e1626; border: 4px solid #26365a; opacity: 0.35; }}
.bt {{ position: absolute; left: 24px; top: 16px; font-size: 34px; font-weight: 700; }}
.bc {{ position: absolute; left: 0; width: 420px; text-align: center; font-family: "JetBrains Mono", monospace; font-weight: 700; white-space: nowrap; }}
</style>
<div id="root" data-composition-id="world" data-width="1920" data-height="1080">
  {B1}{B2}{B3}{B4}
  <div id="caps"></div>
</div>
<script>
/*PRE*/
/*HW*/
/*T*/
const CAPS = ["Підсумок уроку", "while повторює, поки умова істинна", "for перебирає елементи через ітератор", "range лише обчислює числа", "break, continue і else керують ходом циклу"];
{CAPJS}
tl.set(["#k1", "#k2", "#k3", "#k4"], {{ opacity: 0.35 }}, 0);
pulse("#k1", 0.6, 1.02);
[1, 2, 3, 4].forEach((k, i) => {{ tl.to("#k" + k, {{ opacity: 1, duration: 0.4 }}, T[i + 1] + 0.3); pulse("#k" + k, T[i + 1] + 0.8, 1.05); pulse("#k" + k, T[i + 1] + 2.0, 1.03); pulse("#k" + k, T[i + 1] + 3.0, 1.03); }});
window.__timelines["world"] = tl;
</script>
''')
