//! Computational graph + backward: z = x^2 + 3xy + y^2, x=2 y=3 z=31.
//! Forward pulses 1.0-4.5 (cyan), backward pulses 4.8-8.8 (amber), loop fade 9.2-10.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct CgMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

const BG_COLOR: &str = "#070b14";
const CARD_BG: &str = "#0f172a";
const CARD_BORDER: &str = "#1e293b";

const TEXT_MAIN: &str = "#f8fafc";
const TEXT_MUTED: &str = "#94a3b8";
const TEXT_DIM: &str = "#64748b";

const COLOR_CYAN: &str = "#38bdf8";
const COLOR_INDIGO: &str = "#818cf8";
const COLOR_EMERALD: &str = "#10b981";
const COLOR_AMBER: &str = "#f59e0b";
const COLOR_ROSE: &str = "#f43f5e";

#[inline]
fn clamp(v: f32, min: f32, max: f32) -> f32 {
    v.max(min).min(max)
}

#[inline]
fn ease_out_cubic(t: f32) -> f32 {
    let t = clamp(t, 0.0, 1.0);
    1.0 - (1.0 - t).powi(3)
}

#[inline]
fn ease_in_out(t: f32) -> f32 {
    let t = clamp(t, 0.0, 1.0);
    if t < 0.5 {
        4.0 * t * t * t
    } else {
        1.0 - (-2.0 * t + 2.0).powi(3) / 2.0
    }
}

#[inline]
fn lerp(a: f32, b: f32, p: f32) -> f32 {
    a + (b - a) * p
}

pub struct CgVideo<'a> {
    pub media: &'a CgMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> CgVideo<'a> {
    pub fn new(media: &'a CgMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for CgVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CgVideo").finish()
    }
}

impl fframes::Video for CgVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.2)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(2.6)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(4.2)..AudioTimestamp::Eof)
                .gain_db(0.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(5.4)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(7.4)..AudioTimestamp::Eof)
                .gain_db(0.0),
        ])
    }

    fn render_frame<'a>(&'a self, frame: Frame, _ctx: &FFramesContext<'a, '_>) -> Svgr<'a> {
        let t = frame.seconds();

        let intro_alpha = ease_out_cubic(clamp(t / 0.8, 0.0, 1.0));
        let loop_reset = if t >= 9.2 {
            1.0 - ease_in_out(clamp((t - 9.2) / 0.8, 0.0, 1.0))
        } else {
            1.0
        };
        let g_alpha = intro_alpha * loop_reset;

        // Forward phase progress
        let fw = ease_in_out(clamp((t - 1.0) / 3.2, 0.0, 1.0));
        // Backward phase progress
        let bw = ease_in_out(clamp((t - 4.8) / 3.6, 0.0, 1.0));

        // Node centers
        let (xx, xy_) = (300.0, 360.0);
        let (yx, yy_) = (300.0, 640.0);
        let (x2x, x2y) = (700.0, 290.0);
        let (midx, midy) = (700.0, 500.0);
        let (y2x, y2y) = (700.0, 710.0);
        let (s1x, s1y) = (1100.0, 400.0);
        let (zx, zy) = (1500.0, 500.0);

        // Forward pulse positions (cyan): travel leaf -> mid -> sum -> z
        let fp1 = clamp((t - 1.2) / 2.8, 0.0, 1.0);
        let f1x = lerp(xx, x2x, fp1);
        let f1y = lerp(xy_, x2y, fp1);
        let f2x = lerp(xx, midx, clamp((t - 1.5) / 2.8, 0.0, 1.0));
        let f2y = lerp(xy_, midy, clamp((t - 1.5) / 2.8, 0.0, 1.0));
        let f3x = lerp(yx, y2x, clamp((t - 1.5) / 2.8, 0.0, 1.0));
        let f3y = lerp(yy_, y2y, clamp((t - 1.5) / 2.8, 0.0, 1.0));
        let f4x = lerp(midx, s1x, clamp((t - 2.6) / 2.0, 0.0, 1.0));
        let f4y = lerp(midy, s1y, clamp((t - 2.6) / 2.0, 0.0, 1.0));
        let f5x = lerp(s1x, zx, clamp((t - 3.2) / 1.6, 0.0, 1.0));
        let f5y = lerp(s1y, zy, clamp((t - 3.2) / 1.6, 0.0, 1.0));
        let fw_on = if t > 1.0 && t < 4.8 { 1.0 } else { 0.0 };

        // Backward pulses (amber): z -> sum -> mid -> leaf
        let b1x = lerp(zx, s1x, clamp((t - 5.0) / 2.8, 0.0, 1.0));
        let b1y = lerp(zy, s1y, clamp((t - 5.0) / 2.8, 0.0, 1.0));
        let b2x = lerp(s1x, midx, clamp((t - 5.8) / 2.4, 0.0, 1.0));
        let b2y = lerp(s1y, midy, clamp((t - 5.8) / 2.4, 0.0, 1.0));
        let b3x = lerp(midx, xx, clamp((t - 6.6) / 2.0, 0.0, 1.0));
        let b3y = lerp(midy, xy_, clamp((t - 6.6) / 2.0, 0.0, 1.0));
        let b4x = lerp(y2x, yx, clamp((t - 6.6) / 2.0, 0.0, 1.0));
        let b4y = lerp(y2y, yy_, clamp((t - 6.6) / 2.0, 0.0, 1.0));
        let bw_on = if t >= 4.8 && t < 9.0 { 1.0 } else { 0.0 };

        // Value labels appear with forward progress
        let mid_op = clamp((fw - 0.35) / 0.3, 0.0, 1.0);
        let sum_op = clamp((fw - 0.6) / 0.3, 0.0, 1.0);
        let z_op = clamp((fw - 0.85) / 0.15, 0.0, 1.0);
        // Grad labels appear with backward progress
        let g1_op = clamp((bw - 0.15) / 0.2, 0.0, 1.0);
        let g2_op = clamp((bw - 0.45) / 0.2, 0.0, 1.0);
        let g3_op = clamp((bw - 0.7) / 0.25, 0.0, 1.0);

        let phase = if t < 4.6 {
            "FORWARD: прямий прохід, PyTorch будує граф (grad_fn)"
        } else {
            "BACKWARD: .backward() — ланцюгове правило справа наліво"
        };

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <radialGradient id="bg-glow" cx="0.5" cy="0.4" r="0.65">
                        <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.35" />
                        <stop offset="60%" stop-color="#0b1329" stop-opacity="0.10" />
                        <stop offset="100%" stop-color={BG_COLOR} stop-opacity="0" />
                    </radialGradient>
                    <pattern id="dot-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="1.2" fill="#334155" opacity="0.25" />
                    </pattern>
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH / 2} cy={HEIGHT / 2} r="800" fill="url(#bg-glow)" />

                <g opacity={g_alpha}>
                    <rect x="640" y="24" width="640" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "AUTOGRAD: ДИНАМІЧНИЙ ГРАФ ОБЧИСЛЕНЬ + BACKPROPAGATION"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "z = x² + 3xy + y²  (x=2, y=3 → z=31)"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={COLOR_AMBER} text-anchor="middle">
                        {phase}
                    </text>
                </g>

                // ---- Graph canvas ----
                <g opacity={g_alpha}>
                    <rect x="70" y="155" width="1780" height="640" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />

                    // edges (static, dim)
                    <g stroke="#334155" stroke-width="2.5">
                        <line x1={xx + 70.0} y1={xy_} x2={x2x - 80.0} y2={x2y} />
                        <line x1={xx + 70.0} y1={xy_ + 10.0} x2={midx - 80.0} y2={midy - 10.0} />
                        <line x1={yx + 70.0} y1={yy_ - 10.0} x2={midx - 80.0} y2={midy + 10.0} />
                        <line x1={yx + 70.0} y1={yy_} x2={y2x - 80.0} y2={y2y} />
                        <line x1={x2x + 80.0} y1={x2y + 20.0} x2={s1x - 90.0} y2={s1y - 10.0} />
                        <line x1={midx + 80.0} y1={midy - 15.0} x2={s1x - 90.0} y2={s1y + 5.0} />
                        <line x1={y2x + 80.0} y1={y2y - 25.0} x2={zx - 90.0} y2={zy + 15.0} />
                        <line x1={s1x + 90.0} y1={s1y} x2={zx - 90.0} y2={zy} />
                    </g>
                    <text x="490" y="300" font-family={FONT} font-size="12" fill={TEXT_DIM}>"PowBackward"</text>
                    <text x="490" y="500" font-family={FONT} font-size="12" fill={TEXT_DIM}>"MulBackward"</text>
                    <text x="490" y="700" font-family={FONT} font-size="12" fill={TEXT_DIM}>"PowBackward"</text>
                    <text x="880" y="360" font-family={FONT} font-size="12" fill={TEXT_DIM}>"AddBackward"</text>
                    <text x="1290" y="460" font-family={FONT} font-size="12" fill={TEXT_DIM}>"AddBackward"</text>

                    // leaf nodes
                    <g>
                        <rect x={xx - 75.0} y={xy_ - 42.0} width="150" height="84" rx="14" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="2" />
                        <text x={xx} y={xy_ - 6.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"x = 2.0"</text>
                        <text x={xx} y={xy_ + 20.0} font-family={FONT} font-size="12" fill={COLOR_CYAN} text-anchor="middle">"leaf, requires_grad"</text>
                    </g>
                    <g>
                        <rect x={yx - 75.0} y={yy_ - 42.0} width="150" height="84" rx="14" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="2" />
                        <text x={yx} y={yy_ - 6.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"y = 3.0"</text>
                        <text x={yx} y={yy_ + 20.0} font-family={FONT} font-size="12" fill={COLOR_CYAN} text-anchor="middle">"leaf, requires_grad"</text>
                    </g>

                    // mid nodes
                    <g opacity={mid_op}>
                        <rect x={x2x - 80.0} y={x2y - 42.0} width="160" height="84" rx="14" fill="#1e293b" stroke={COLOR_INDIGO} stroke-width="2" />
                        <text x={x2x} y={x2y - 4.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"x² = 4"</text>
                        <text x={x2x} y={x2y + 22.0} font-family={FONT} font-size="12" fill={TEXT_MUTED} text-anchor="middle">"PowBackward0"</text>
                    </g>
                    <g opacity={mid_op}>
                        <rect x={midx - 85.0} y={midy - 42.0} width="170" height="84" rx="14" fill="#1e293b" stroke={COLOR_INDIGO} stroke-width="2" />
                        <text x={midx} y={midy - 4.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3xy = 18"</text>
                        <text x={midx} y={midy + 22.0} font-family={FONT} font-size="12" fill={TEXT_MUTED} text-anchor="middle">"MulBackward0"</text>
                    </g>
                    <g opacity={mid_op}>
                        <rect x={y2x - 80.0} y={y2y - 42.0} width="160" height="84" rx="14" fill="#1e293b" stroke={COLOR_INDIGO} stroke-width="2" />
                        <text x={y2x} y={y2y - 4.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"y² = 9"</text>
                        <text x={y2x} y={y2y + 22.0} font-family={FONT} font-size="12" fill={TEXT_MUTED} text-anchor="middle">"PowBackward0"</text>
                    </g>
                    <g opacity={sum_op}>
                        <rect x={s1x - 95.0} y={s1y - 42.0} width="190" height="84" rx="14" fill="#1e293b" stroke={COLOR_INDIGO} stroke-width="2" />
                        <text x={s1x} y={s1y - 4.0} font-family={FONT} font-size="22" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"x²+3xy = 22"</text>
                        <text x={s1x} y={s1y + 22.0} font-family={FONT} font-size="12" fill={TEXT_MUTED} text-anchor="middle">"AddBackward0"</text>
                    </g>
                    <g opacity={z_op}>
                        <rect x={zx - 95.0} y={zy - 46.0} width="190" height="92" rx="14" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2.5" />
                        <text x={zx} y={zy - 6.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"z = 31.0"</text>
                        <text x={zx} y={zy + 20.0} font-family={FONT} font-size="12" fill={COLOR_EMERALD} text-anchor="middle">"grad_fn = AddBackward0"</text>
                    </g>

                    // forward pulses
                    <g opacity={fw_on * g_alpha}>
                        <circle cx={f1x} cy={f1y} r="9" fill={COLOR_CYAN} />
                        <circle cx={f2x} cy={f2y} r="9" fill={COLOR_CYAN} />
                        <circle cx={f3x} cy={f3y} r="9" fill={COLOR_CYAN} />
                        <circle cx={f4x} cy={f4y} r="9" fill={COLOR_CYAN} />
                        <circle cx={f5x} cy={f5y} r="10" fill={COLOR_EMERALD} />
                    </g>
                    // backward pulses
                    <g opacity={bw_on * g_alpha}>
                        <circle cx={b1x} cy={b1y} r="10" fill={COLOR_AMBER} />
                        <circle cx={b2x} cy={b2y} r="9" fill={COLOR_AMBER} />
                        <circle cx={b3x} cy={b3y} r="9" fill={COLOR_ROSE} />
                        <circle cx={b4x} cy={b4y} r="9" fill={COLOR_ROSE} />
                    </g>

                    // grad labels
                    <g opacity={g1_op * g_alpha}>
                        <rect x={zx - 90.0} y={zy + 60.0} width="180" height="34" rx="8" fill="#451a03" stroke={COLOR_AMBER} stroke-width="1.5" />
                        <text x={zx} y={zy + 83.0} font-family={FONT} font-size="16" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">"dz/dz = 1.0"</text>
                    </g>
                    <g opacity={g2_op * g_alpha}>
                        <rect x={s1x - 110.0} y={s1y + 55.0} width="220" height="34" rx="8" fill="#451a03" stroke={COLOR_AMBER} stroke-width="1.5" />
                        <text x={s1x} y={s1y + 78.0} font-family={FONT} font-size="15" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">"ланцюгове правило"</text>
                    </g>
                    <g opacity={g3_op * g_alpha}>
                        <rect x={xx - 95.0} y={xy_ + 55.0} width="190" height="40" rx="8" fill="#4c0519" stroke={COLOR_ROSE} stroke-width="1.5" />
                        <text x={xx} y={xy_ + 81.0} font-family={FONT} font-size="17" font-weight="700" fill={COLOR_ROSE} text-anchor="middle">"x.grad = 13.0"</text>
                        <rect x={yx - 95.0} y={yy_ + 55.0} width="190" height="40" rx="8" fill="#4c0519" stroke={COLOR_ROSE} stroke-width="1.5" />
                        <text x={yx} y={yy_ + 81.0} font-family={FONT} font-size="17" font-weight="700" fill={COLOR_ROSE} text-anchor="middle">"y.grad = 12.0"</text>
                    </g>
                </g>

                // ---- Bottom formula bar ----
                <g opacity={g_alpha}>
                    <rect x="70" y="815" width="1780" height="195" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g transform="translate(110, 860)">
                        <text x="0" y="0" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">"АНАЛІТИЧНА ПЕРЕВІРКА (CHAIN RULE)"</text>
                        <text x="0" y="36" font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN}>"dz/dx = 2x + 3y = 2·2 + 3·3 ="</text>
                        <text x="470" y="36" font-family={FONT} font-size="22" font-weight="700" fill={COLOR_ROSE}>"13"</text>
                        <text x="0" y="70" font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN}>"dz/dy = 3x + 2y = 3·2 + 2·3 ="</text>
                        <text x="470" y="70" font-family={FONT} font-size="22" font-weight="700" fill={COLOR_ROSE}>"12"</text>
                        <text x="0" y="104" font-family={FONT} font-size="14" fill={TEXT_MUTED}>"z.backward() проходить граф у зворотному напрямку та складає часткові похідні автоматично"</text>
                    </g>
                    <g transform="translate(1350, 845)">
                        <rect x="0" y="0" width="460" height="135" rx="12" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x="230" y="32" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"КОД: 3 РЯДКИ ЗАМІСТЬ РУЧНИХ ФОРМУЛ"</text>
                        <text x="230" y="62" font-family={FONT} font-size="15" fill={TEXT_MAIN} text-anchor="middle">"x = tensor(2.0, requires_grad=True)"</text>
                        <text x="230" y="86" font-family={FONT} font-size="15" fill={TEXT_MAIN} text-anchor="middle">"z = x**2 + 3*x*y + y**2; z.backward()"</text>
                        <text x="230" y="112" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"x.grad → 13.0 | y.grad → 12.0"</text>
                    </g>
                </g>
            </svg>
        )
    }
}
