const $ = (id) => document.getElementById(id);
const IDV = "4380162600";
// object plaque: type / id / value
const PQ = (p, left, top, w, h, type, val, vcol, idv) => `<div id="${p}" class="card" style="left:${left}px;top:${top}px;width:${w}px;height:${h}px;border-color:#34d399;opacity:0">
  <div id="${p}t" class="abs" style="left:28px;top:20px;width:${w - 56}px;height:${h * 0.22}px;border:3px solid transparent;border-radius:12px;display:flex;align-items:center;gap:20px;padding:0 14px"><span class="lab" style="position:static;font-size:30px">тип</span><span class="mono" style="font-size:${Math.round(h * 0.14)}px;color:#22d3ee">${type}</span></div>
  <div id="${p}v" class="abs" style="left:28px;top:${h * 0.28}px;width:${w - 56}px;height:${h * 0.38}px;border:3px solid transparent;border-radius:12px;display:flex;align-items:center;gap:20px;padding:0 14px"><span class="lab" style="position:static;font-size:30px">значення</span><span class="mono" style="font-size:${Math.round(h * 0.26)}px;color:${vcol}">${val}</span></div>
  <div id="${p}i" class="abs" style="left:28px;top:${h * 0.72}px;width:${w - 56}px;height:${h * 0.2}px;border:3px solid transparent;border-radius:12px;display:flex;align-items:center;gap:20px;padding:0 14px"><span class="lab" style="position:static;font-size:30px">id</span><span class="mono" style="font-size:${Math.round(h * 0.09)}px;color:#fbbf24">${idv || IDV}</span></div></div>`;
const hf = (sel, col, at) => tl.to(sel, { borderColor: col, duration: 0.25 }, at);
const uf = (sel, at) => tl.to(sel, { borderColor: "transparent", duration: 0.25 }, at);
