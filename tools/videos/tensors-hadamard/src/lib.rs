//! Hadamard (A*B) vs Matmul (A@B): A=[[1,2],[3,4]], B=[[5,6],[7,8]].
//! Left: elementwise pops. Right: row x col dot products. 10s loop, dark.

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
const COLOR_EMERALD: &str = "#10b981";
const COLOR_ROSE: &str = "#f43f5e";
const COLOR_AMBER: &str = "#f59e0b";

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
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.4)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(3.4)..AudioTimestamp::Eof)
                .gain_db(0.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.8)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(6.8)..AudioTimestamp::Eof)
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

        // Hadamard reveal 1.2 -> 3.6, staggered per cell
        let hp = clamp((t - 1.2) / 2.4, 0.0, 1.0);
        let h_op = [
            clamp((hp - 0.00) / 0.20, 0.0, 1.0),
            clamp((hp - 0.25) / 0.20, 0.0, 1.0),
            clamp((hp - 0.50) / 0.20, 0.0, 1.0),
            clamp((hp - 0.75) / 0.20, 0.0, 1.0),
        ];
        // Matmul reveal 4.4 -> 7.2
        let mp = clamp((t - 4.4) / 2.8, 0.0, 1.0);
        let m_op = [
            clamp((mp - 0.00) / 0.20, 0.0, 1.0),
            clamp((mp - 0.25) / 0.20, 0.0, 1.0),
            clamp((mp - 0.50) / 0.20, 0.0, 1.0),
            clamp((mp - 0.75) / 0.20, 0.0, 1.0),
        ];
        // Current matmul focus cell (for row/col highlight): last revealed
        let focus = if mp < 0.25 {
            0
        } else if mp < 0.50 {
            1
        } else if mp < 0.75 {
            2
        } else {
            3
        };
        let frow = focus / 2;
        let fcol = focus % 2;

        let warn_op = clamp((t - 7.4) / 0.6, 0.0, 1.0);

        // ---- Left panel geometry (Hadamard) ----
        // mini A at (150,300) cells 84; mini B at (400,300); R cells 120 at (150,540)
        let mc = 84.0;
        let mg = 10.0;
        // ---- Right panel geometry (Matmul), origin shift +940 ----
        // mini A at (1090,300); mini B at (1340,300); R at (1090,540) cells 120

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
                    <rect x="620" y="24" width="680" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_ROSE} text-anchor="middle" letter-spacing="1.5">
                        "ПАСТКА ОПЕРАТОРА *: ПОЕЛЕМЕНТНО ≠ МАТРИЧНО"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "A * B проти A @ B: та сама пара — інший результат"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "A = [[1,2],[3,4]], B = [[5,6],[7,8]]  →  дивіться, як народжуються 4 клітинки результату"
                    </text>
                </g>

                // ============ LEFT: HADAMARD ============
                <g opacity={g_alpha}>
                    <rect x="70" y="155" width="880" height="640" rx="18" fill={CARD_BG} stroke={COLOR_CYAN} stroke-width="1.5" stroke-opacity="0.5" />
                    <rect x="95" y="175" width="440" height="30" rx="8" fill="#1e293b" />
                    <text x="110" y="195" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">
                        "A * B: ПОЕЛЕМЕНТНЕ (HADAMARD), c[i,j] = a[i,j]·b[i,j]"
                    </text>
                    // mini A
                    <g>
                        <text x="150" y="280" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED}>"A"</text>
                        <rect x="150" y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={150.0 + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"1"</text>
                        <rect x={150.0 + mc + mg} y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={150.0 + mc + mg + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"2"</text>
                        <rect x="150" y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={150.0 + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3"</text>
                        <rect x={150.0 + mc + mg} y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={150.0 + mc + mg + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"4"</text>
                    </g>
                    <text x="350" y="395" font-family={FONT} font-size="30" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"×"</text>
                    // mini B
                    <g>
                        <text x="410" y="280" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED}>"B"</text>
                        <rect x="410" y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={410.0 + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"5"</text>
                        <rect x={410.0 + mc + mg} y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={410.0 + mc + mg + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"6"</text>
                        <rect x="410" y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={410.0 + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"7"</text>
                        <rect x={410.0 + mc + mg} y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={410.0 + mc + mg + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"8"</text>
                    </g>
                    <text x="620" y="395" font-family={FONT} font-size="30" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"="</text>
                    // result R (bigger cells)
                    <g>
                        <text x="680" y="280" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_CYAN}>"A*B"</text>
                        <g opacity={h_op[0]}>
                            <rect x="680" y="295" width="110" height="86" rx="10" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="2" />
                            <text x="735" y="348" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"5"</text>
                        </g>
                        <g opacity={h_op[1]}>
                            <rect x="800" y="295" width="110" height="86" rx="10" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="2" />
                            <text x="855" y="348" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"12"</text>
                        </g>
                        <g opacity={h_op[2]}>
                            <rect x="680" y="391" width="110" height="86" rx="10" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="2" />
                            <text x="735" y="444" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"21"</text>
                        </g>
                        <g opacity={h_op[3]}>
                            <rect x="800" y="391" width="110" height="86" rx="10" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="2" />
                            <text x="855" y="444" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"32"</text>
                        </g>
                    </g>
                    // formula line
                    <g transform="translate(150, 560)">
                        <text x="0" y="0" font-family={FONT} font-size="14" fill={TEXT_DIM}>"вимога: ідентичні форми (2,2) і (2,2)"</text>
                        <text x="0" y="40" font-family={FONT} font-size="22" font-weight="700" fill={TEXT_MAIN}>"1·5=5   2·6=12"</text>
                        <text x="0" y="76" font-family={FONT} font-size="22" font-weight="700" fill={TEXT_MAIN}>"3·7=21   4·8=32"</text>
                        <text x="0" y="116" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"кожен елемент — незалежна пара"</text>
                        <text x="0" y="146" font-family={FONT} font-size="14" fill={TEXT_DIM}>"broadcasting теж працює, якщо форми сумісні"</text>
                    </g>
                </g>

                // ============ RIGHT: MATMUL ============
                <g opacity={g_alpha}>
                    <rect x="990" y="155" width="860" height="640" rx="18" fill={CARD_BG} stroke={COLOR_EMERALD} stroke-width="1.5" stroke-opacity="0.6" />
                    <rect x="1015" y="175" width="560" height="30" rx="8" fill="#1e293b" />
                    <text x="1030" y="195" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD} letter-spacing="1.0">
                        "A @ B: МАТРИЧНЕ, c[i,j] = РЯДОК i · СТОВПЕЦЬ j"
                    </text>
                    // mini A with row highlight
                    <g>
                        <text x="1070" y="280" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED}>"A"</text>
                        <rect x="1070" y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1070.0 + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"1"</text>
                        <rect x={1070.0 + mc + mg} y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1070.0 + mc + mg + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"2"</text>
                        <rect x="1070" y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1070.0 + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3"</text>
                        <rect x={1070.0 + mc + mg} y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1070.0 + mc + mg + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"4"</text>
                        // row highlight band
                        <rect x="1070" y={if frow == 0 { 295.0 } else { 295.0 + mc + mg }} width={2.0 * mc + mg} height={mc} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={mp.min(1.0)} />
                    </g>
                    <text x="1270" y="395" font-family={FONT} font-size="30" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"×"</text>
                    // mini B with col highlight
                    <g>
                        <text x="1330" y="280" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED}>"B"</text>
                        <rect x="1330" y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1330.0 + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"5"</text>
                        <rect x={1330.0 + mc + mg} y="295" width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1330.0 + mc + mg + mc / 2.0} y={295.0 + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"6"</text>
                        <rect x="1330" y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1330.0 + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"7"</text>
                        <rect x={1330.0 + mc + mg} y={295.0 + mc + mg} width={mc} height={mc} rx="8" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                        <text x={1330.0 + mc + mg + mc / 2.0} y={295.0 + mc + mg + mc / 2.0 + 8.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"8"</text>
                        // col highlight band
                        <rect x={if fcol == 0 { 1330.0 } else { 1330.0 + mc + mg }} y="295" width={mc} height={2.0 * mc + mg} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={mp.min(1.0)} />
                    </g>
                    <text x="1540" y="395" font-family={FONT} font-size="30" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"="</text>
                    // result R
                    <g>
                        <text x="1600" y="280" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD}>"A@B"</text>
                        <g opacity={m_op[0]}>
                            <rect x="1600" y="295" width="110" height="86" rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                            <text x="1655" y="348" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"19"</text>
                        </g>
                        <g opacity={m_op[1]}>
                            <rect x="1720" y="295" width="110" height="86" rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                            <text x="1775" y="348" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"22"</text>
                        </g>
                        <g opacity={m_op[2]}>
                            <rect x="1600" y="391" width="110" height="86" rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                            <text x="1655" y="444" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"43"</text>
                        </g>
                        <g opacity={m_op[3]}>
                            <rect x="1720" y="391" width="110" height="86" rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                            <text x="1775" y="444" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"50"</text>
                        </g>
                    </g>
                    // formula line
                    <g transform="translate(1070, 560)">
                        <text x="0" y="0" font-family={FONT} font-size="14" fill={TEXT_DIM}>"вимога: внутрішні виміри (m×k)@(k×n) = (m×n)"</text>
                        <text x="0" y="40" font-family={FONT} font-size="22" font-weight="700" fill={TEXT_MAIN}>"1·5+2·7=19   1·6+2·8=22"</text>
                        <text x="0" y="76" font-family={FONT} font-size="22" font-weight="700" fill={TEXT_MAIN}>"3·5+4·7=43   3·6+4·8=50"</text>
                        <text x="0" y="116" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"кожен елемент — скалярний добуток"</text>
                        <text x="0" y="146" font-family={FONT} font-size="14" fill={TEXT_DIM}>"@ = torch.matmul = torch.mm (для 2D)"</text>
                    </g>
                </g>

                // ---- Bottom warning ----
                <g opacity={(warn_op * g_alpha).min(1.0)}>
                    <rect x="70" y="820" width="1780" height="190" rx="18" fill="#4c0519" stroke={COLOR_ROSE} stroke-width="2" />
                    <text x="960" y="872" font-family={FONT} font-size="20" font-weight="700" fill={COLOR_ROSE} text-anchor="middle">
                        "НЕЙРОМЕРЕЖІ ЖИВУТЬ НА @ : y = X @ W + b — лінійний шар, а не поелементне множення"
                    </text>
                    <text x="960" y="908" font-family={FONT} font-size="16" fill={TEXT_MAIN} text-anchor="middle">
                        "[[19,22],[43,50]] vs [[5,12],[21,32]] — переплутав оператор і модель мовчки рахує нісенітницю"
                    </text>
                    <text x="960" y="944" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        "NumPy поводиться так само: * — поелементно, @ — матрично (Python 3.5+)"
                    </text>
                </g>
            </svg>
        )
    }
}
