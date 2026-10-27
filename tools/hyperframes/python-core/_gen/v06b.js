<script>
/*PRE*/
/*HW*/
/*T*/
const barY = (k) => 112 + k * 58;
// L1 pills
tl.set("#cs", { opacity: 1 }, 0);
show("#pl1", T[0] + 0.5); show("#pl2", T[0] + 0.9); pulse("#pl1", T[0] + 1.2, 1.06); pulse("#pl2", T[0] + 1.5, 1.06);
// L2 compiler takes the whole file
tl.to("#pl1", { borderColor: "#22d3ee", color: "#22d3ee", duration: 0.3 }, T[1] + 0.2);
tl.set("#cbar", { height: 168 }, 0);
show("#cbar", T[1] + 1.2, 0.3);
show("#car1", T[1] + 1.6); show("#cbx", T[1] + 1.7); pulse("#cbx", T[1] + 2.1, 1.08);
show("#car2", T[1] + 2.3); show("#cexe", T[1] + 2.4, 0.3);
for (let k = 0; k < 3; k++) typeIn("#ch" + k, 26, T[1] + 2.8 + k * 0.5, 0.5);
// L3 ready file; source not needed
pulse("#cexe", T[2] + 0.3, 1.03);
for (let k = 0; k < 3; k++) tl.to("#ch" + k, { color: "#e8eef7", duration: 0.2 }, T[2] + 1.6 + k * 0.2);
tl.to("#ced", { opacity: 0.5, duration: 0.5 }, T[2] + 3.0); hide("#cbar", T[2] + 3.0, 0.3);
show("#cnote", T[2] + 3.3); pulse("#cbx", T[2] + 4.1, 1.08); pulse("#cexe", T[2] + 4.9, 1.03); pulse("#cnote", T[2] + 5.5, 1.04);
// L4 run it
show("#cc", T[3] + 0.2, 0.05); typeIn("#ccy", 11, T[3] + 0.3, 0.6);
for (let k = 0; k < 3; k++) show("#co" + k, T[3] + 1.3, 0.05);
pulse("#cterm", T[3] + 1.5, 1.03);
// L5 interpreter reads, translates, executes one line
hide("#cs", T[4] - 0.4, 0.35);
tl.to("#is", { opacity: 1, duration: 0.3 }, T[4] - 0.05);
tl.to("#pl1", { borderColor: "#26365a", color: "#9fb2cf", duration: 0.2 }, T[4]);
tl.to("#pl2", { borderColor: "#34d399", color: "#34d399", duration: 0.3 }, T[4] + 0.2);
show("#iar1", T[4] + 0.8); show("#ibx", T[4] + 0.9);
tl.set("#ibar", { height: 54 }, 0);
show("#ibar", T[4] + 2.0, 0.2);
show("#iar2", T[4] + 2.8); typeIn("#ih0", 26, T[4] + 3.0, 0.5);
show("#ic", T[4] + 3.4, 0.05); typeIn("#icy", 21, T[4] + 3.5, 0.8);
show("#io0", T[4] + 4.5, 0.1); pulse("#io0", T[4] + 4.5, 1.1);
// L6 next lines, translated each time
const mv = (k, a) => tl.to("#ibar", { y: k * 58, duration: 0.25 }, a);
mv(1, T[5] + 0.3); tl.to("#ih0", { opacity: 0, duration: 0.15 }, T[5] + 0.8); tl.set("#ih1", { width: 0 }, 0); typeIn("#ih1", 26, T[5] + 1.0, 0.5); show("#io1", T[5] + 1.6, 0.1); pulse("#io1", T[5] + 1.6, 1.1);
mv(2, T[5] + 2.4); tl.to("#ih1", { opacity: 0, duration: 0.15 }, T[5] + 2.9); typeIn("#ih2", 26, T[5] + 3.1, 0.5); show("#io2", T[5] + 3.6, 0.1); pulse("#io2", T[5] + 3.6, 1.1);
show("#inote", T[5] + 4.0);
// L7 both deliver commands to the CPU
hide("#inote", T[6] - 0.1, 0.2);
show("#cpu", T[6] + 0.2); show("#cmdl", T[6] + 0.6); pulse("#cpu", T[6] + 1.0, 1.08);
pulse("#icard", T[6] + 1.4, 1.03);
hide("#pl1", CL - 0.35, 0.3); hide("#pl2", CL - 0.35, 0.3);
window.__timelines["world"] = tl;
</script>
