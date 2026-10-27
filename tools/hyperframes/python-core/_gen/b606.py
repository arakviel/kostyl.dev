G="/private/tmp/claude-501/-Users-arakviel-Work-kostyl-dev/82ea6f59-25c7-47d3-a3df-29a1c293aa8e/scratchpad/gen/"
CAPCSS='.cpt { position: absolute; left: 80px; width: 1760px; top: 975px; text-align: center; font-size: 40px; font-weight: 700; color: #fbbf24; opacity: 0; }'
CAPJS='''const $ = (id) => document.getElementById(id);
CAPS.forEach((t, i) => { $("caps").insertAdjacentHTML("beforeend", `<div id="cp${i}" class="cpt">${t}</div>`); show("#cp" + i, T[i] + 0.2, 0.3); hide("#cp" + i, (i < CAPS.length - 1 ? T[i + 1] - 0.15 : CL - 0.35), 0.25); });'''
V='<div class="vsb"><span class="vsd" style="left:20px;background:#ff5f57"></span><span class="vsd" style="left:48px;background:#febc2e"></span><span class="vsd" style="left:76px;background:#28c840"></span><div class="vsT">%s</div></div><div class="vsr"></div><div class="vst">%s</div>'
K='<span style="color:#c586c0">%s</span>'
def N(x): return f'<span style="color:#b5cea8">{x}</span>'
def L(k,n,html,fs=36): return f'<div class="vsl" style="top:{118+k*54}px;font-size:{fs}px"><span class="n">{n}</span><span style="white-space:pre">{html}</span></div>'
loop1=[K%'for'+' <span style="color:#9cdcfe">i</span> '+K%'in'+' <span style="color:#dcdcaa">range</span>('+N(1)+', '+N(6)+'):',
 '    '+K%'if'+' <span style="color:#9cdcfe">i</span> == '+N(2)+':', '        '+K%'continue', '    '+K%'if'+' <span style="color:#9cdcfe">i</span> == '+N(5)+':', '        '+K%'break', '    <span style="color:#dcdcaa">print</span>(<span style="color:#9cdcfe">i</span>, <span style="color:#9cdcfe">end</span>=<span style="color:#ce9178">" "</span>)']
code1="".join(L(i,i+1,l) for i,l in enumerate(loop1))
prime=['<span style="color:#9cdcfe">n</span> = '+N(17), K%'for'+' <span style="color:#9cdcfe">d</span> '+K%'in'+' <span style="color:#dcdcaa">range</span>('+N(2)+', <span style="color:#9cdcfe">n</span>):', '    '+K%'if'+' <span style="color:#9cdcfe">n</span> % <span style="color:#9cdcfe">d</span> == '+N(0)+':', '        <span style="color:#dcdcaa">print</span>(<span style="color:#9cdcfe">n</span>, <span style="color:#ce9178">"складене, дільник"</span>, <span style="color:#9cdcfe">d</span>)', '        '+K%'break', K%'else'+':', '    <span style="color:#dcdcaa">print</span>(<span style="color:#9cdcfe">n</span>, <span style="color:#ce9178">"просте"</span>)']
code2="".join(L(i,i+1,l,30) for i,l in enumerate(prime))
chips="".join(f'<div id="ic{i}" class="ic" style="left:{1000+i*168}px"><div class="mono">i={i+1}</div><div id="ia{i}" class="ia">{a}</div></div>' for i,a in enumerate(["print","continue","print","print","break"]))
dchips="".join(f'<div id="dc{d}" class="dc" style="left:{70+(d-2)*112}px">{d}</div>' for d in range(2,17))
open(G+"z606.part","w").write(f'''<style>
{CAPCSS}
.ic {{ position: absolute; top: 380px; width: 150px; height: 130px; border-radius: 16px; background: #0e1626; border: 4px solid #26365a; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; font-size: 32px; font-weight: 700; color: #9fb2cf; }}
.ia {{ font-family: "JetBrains Mono", monospace; font-size: 28px; color: #6f84a6; }}
.dc {{ position: absolute; top: 680px; width: 96px; height: 96px; border-radius: 14px; background: #0e1626; border: 4px solid #26365a; display: flex; align-items: center; justify-content: center; font-family: "JetBrains Mono", monospace; font-weight: 800; font-size: 40px; color: #9fb2cf; opacity: 0; }}
</style>
<div id="root" data-composition-id="world" data-width="1920" data-height="1080">
  <div id="ed1" class="vsw" style="left:60px;top:100px;width:880px;height:460px">{V%("loop.py","loop.py")}{code1}
    <div id="hl1" style="position:absolute;left:0;width:880px;height:54px;top:118px;background:rgba(251,191,36,0.2);opacity:0"></div></div>
  <div id="g1">{chips}
    <div id="t1" class="vsw" style="left:1000px;top:100px;width:840px;height:220px"><div class="vsb"><div class="vsT" style="text-align:left;left:24px">ТЕРМІНАЛ</div></div>
      <div id="s1" class="mono abs" style="left:24px;top:90px;font-size:56px;color:#34d399;opacity:0">1</div><div id="s2" class="mono abs" style="left:100px;top:90px;font-size:56px;color:#34d399;opacity:0">3</div><div id="s3" class="mono abs" style="left:176px;top:90px;font-size:56px;color:#34d399;opacity:0">4</div></div>
  </div>
  <div id="ed2" class="vsw" style="left:60px;top:100px;width:980px;height:520px;opacity:0">{V%("prime.py","prime.py")}{code2}
    <div id="hl2" style="position:absolute;left:0;width:980px;height:54px;top:118px;background:rgba(251,191,36,0.2);opacity:0"></div></div>
  <div id="g2" style="opacity:0">{dchips}</div>
  <div id="t2" class="vsw" style="left:1100px;top:100px;width:740px;height:220px;opacity:0"><div class="vsb"><div class="vsT" style="text-align:left;left:24px">ТЕРМІНАЛ</div></div>
    <div id="p1" class="vsx" style="top:90px;font-size:56px;color:#34d399;font-weight:700">17 просте</div></div>
  <div id="caps"></div>
</div>
<script>
/*PRE*/
/*HW*/
/*T*/
const CAPS = ["break завершує цикл одразу", "continue пропускає решту ітерації й повертається до початку циклу", "i == 2 → continue (пропуск), i == 5 → break (вихід). Виводиться: 1 3 4", "else виконується, тільки якщо цикл дійшов до кінця без break", "17: дільника немає, break не спрацював → виконується else: «просте»"];
{CAPJS}
const row = (k) => k * 54;
tl.set("#ed1", {{ opacity: 1 }}, 0);
// L1 break
tl.set("#hl1", {{ y: row(4), opacity: 1 }}, T[0] + 0.5); pulse("#ed1", T[0] + 1.2, 1.02);
// L2 continue
tl.set("#hl1", {{ y: row(2) }}, T[1] + 0.5); pulse("#ed1", T[1] + 1.4, 1.02);
// L3 iterations 1..5
const steps = [[5, "print"], [2, "continue"], [5, "print"], [5, "print"], [4, "break"]];
const col = {{ print: "#34d399", continue: "#fbbf24", break: "#fb7185" }};
steps.forEach(([ln, a], i) => {{ const at = T[2] + 0.6 + i * 1.25;
  tl.set("#hl1", {{ y: row(ln) }}, at); tl.to("#ic" + i, {{ borderColor: col[a], duration: 0.2 }}, at); tl.to("#ia" + i, {{ color: col[a], duration: 0.2 }}, at); pulse("#ic" + i, at, 1.08); }});
show("#s1", T[2] + 0.9, 0.1); show("#s2", T[2] + 3.4, 0.1); show("#s3", T[2] + 4.65, 0.1); tl.set("#hl1", {{ opacity: 0 }}, T[2] + 7.0);
// L4 else after the loop
hide("#ed1", T[3] + 0.1, 0.3); hide("#g1", T[3] + 0.1, 0.3); show("#ed2", T[3] + 0.5, 0.3);
tl.set("#hl2", {{ y: row(5), opacity: 1 }}, T[3] + 1.4); pulse("#ed2", T[3] + 3.4, 1.01);
// L5 17: no divisor
tl.set("#hl2", {{ y: row(2) }}, T[4] + 0.4); show("#g2", T[4] + 0.4, 0.2);
for (let d = 2; d <= 16; d++) show("#dc" + d, T[4] + 0.6 + (d - 2) * 0.22, 0.1);
tl.set("#hl2", {{ y: row(5) }}, T[4] + 4.2); show("#t2", T[4] + 4.4, 0.3); show("#p1", T[4] + 4.8, 0.1); pulse("#p1", T[4] + 4.9, 1.1);
["#ed2", "#g2", "#t2"].forEach((x) => hide(x, CL - 0.35, 0.3));
window.__timelines["world"] = tl;
</script>
''')
