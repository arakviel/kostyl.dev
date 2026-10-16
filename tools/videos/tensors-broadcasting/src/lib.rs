//! Broadcasting visualization: A(2x3) + B(3,) -> R(2x3).
//!
//! Timeline (10s, 16:9, dark):
//! 0.0-0.8 intro fade; 0.8-2.5 show A and B; 2.5-4.5 virtual expansion of B;
//! 4.5-6.5 elementwise add -> result cells pop; 6.5-9.2 shape-rule highlight;
//! 9.2-10.0 seamless loop fade.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct BcMedia, "media");

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

pub struct BcVideo<'a> {
    pub media: &'a BcMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> BcVideo<'a> {
    pub fn new(media: &'a BcMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for BcVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("BcVideo").finish()
    }
}

impl fframes::Video for BcVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(2.5)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(4.8)..AudioTimestamp::Eof)
                .gain_db(0.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(5.6)..AudioTimestamp::Eof)
                .gain_db(-1.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(6.8)..AudioTimestamp::Eof)
                .gain_db(-3.0),
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

        // Expansion progress 2.5 -> 4.0
        let exp_p = ease_in_out(clamp((t - 2.5) / 1.5, 0.0, 1.0));
        // Result reveal 4.5 -> 6.5 (6 cells pop one by one)
        let res_p = clamp((t - 4.5) / 2.0, 0.0, 1.0);
        // Rule highlight pulse 6.8+
        let rule_glow = if t >= 6.8 {
            0.5 + 0.5 * ((t - 6.8) * 3.0).sin().abs()
        } else {
            0.0
        };

        // Geometry: 3 cards
        // Card A: x 70 w 540; Card B: x 650 w 540; Card R: x 1230 w 620; y 165 h 620
        let cell_w = 128.0;
        let cell_h = 78.0;
        let gap = 14.0;

        // A origin (top-left of first cell)
        let ax = 140.0;
        let ay = 330.0;
        // B origin
        let bx = 720.0;
        let by = 330.0;
        // R origin
        let rx = 1300.0;
        let ry = 330.0;

        let a_vals = ["1", "2", "3", "4", "5", "6"];
        let b_vals = ["10", "20", "30"];
        let r_vals = ["11", "22", "33", "14", "25", "36"];

        // Per-cell reveal thresholds for R
        let r_op = [
            clamp((res_p - 0.08) / 0.12, 0.0, 1.0),
            clamp((res_p - 0.22) / 0.12, 0.0, 1.0),
            clamp((res_p - 0.36) / 0.12, 0.0, 1.0),
            clamp((res_p - 0.50) / 0.12, 0.0, 1.0),
            clamp((res_p - 0.64) / 0.12, 0.0, 1.0),
            clamp((res_p - 0.78) / 0.12, 0.0, 1.0),
        ];
        // Ghost row opacity = expansion progress
        let ghost_op = exp_p;
        // Ghost row y offset slides in from above
        let ghost_dy = (1.0 - exp_p) * -30.0;

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
                    <marker id="arrow-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill={COLOR_AMBER} />
                    </marker>
                    <marker id="arrow-emerald" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill={COLOR_EMERALD} />
                    </marker>
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH / 2} cy={HEIGHT / 2} r="800" fill="url(#bg-glow)" />

                <g opacity={g_alpha}>
                    <rect x="700" y="24" width="520" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "ТЕНЗОРИ: МЕХАНІЗМ BROADCASTING БЕЗ КОПІЮВАННЯ ПАМ'ЯТІ"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="32" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "A (2x3) + B (3,) = R (2x3): віртуальне розширення"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "Менший тензор розтягується віртуально: strides = 0, фізичної копії даних немає"
                    </text>
                </g>

                // ---- Card A ----
                <g opacity={g_alpha}>
                    <rect x="70" y="165" width="540" height="620" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="95" y="185" width="300" height="30" rx="8" fill="#1e293b" />
                    <text x="110" y="205" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">
                        "ТЕНЗОР A: МАТРИЦЯ (2, 3)"
                    </text>
                    // A cells 2x3 (static SVG, compile-time svgtree friendly)
                    <g>
                        <rect x={ax} y={ay} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={ax + cell_w / 2.0} y={ay + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"1"</text>
                        <rect x={ax + cell_w + gap} y={ay} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={ax + cell_w + gap + cell_w / 2.0} y={ay + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"2"</text>
                        <rect x={ax + 2.0 * (cell_w + gap)} y={ay} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={ax + 2.0 * (cell_w + gap) + cell_w / 2.0} y={ay + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3"</text>
                        <rect x={ax} y={ay + cell_h + gap} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={ax + cell_w / 2.0} y={ay + cell_h + gap + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"4"</text>
                        <rect x={ax + cell_w + gap} y={ay + cell_h + gap} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={ax + cell_w + gap + cell_w / 2.0} y={ay + cell_h + gap + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"5"</text>
                        <rect x={ax + 2.0 * (cell_w + gap)} y={ay + cell_h + gap} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={ax + 2.0 * (cell_w + gap) + cell_w / 2.0} y={ay + cell_h + gap + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"6"</text>
                    </g>
                    <text x="340" y="560" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        "shape = [2, 3]  |  6 елементів"
                    </text>
                    <text x="340" y="700" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        "[[1, 2, 3],"
                    </text>
                    <text x="340" y="726" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        " [4, 5, 6]]"
                    </text>
                </g>

                // ---- Plus sign between A and B ----
                <g opacity={g_alpha}>
                    <text x="630" y="450" font-family={FONT} font-size="56" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">"+"</text>
                </g>

                // ---- Card B ----
                <g opacity={g_alpha}>
                    <rect x="650" y="165" width="540" height="620" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="675" y="185" width="330" height="30" rx="8" fill="#1e293b" />
                    <text x="690" y="205" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_AMBER} letter-spacing="1.0">
                        "ТЕНЗОР B: ВЕКТОР (3,)"
                    </text>
                    // B original row
                    <g>
                        <rect x={bx} y={by} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_AMBER} stroke-width="1.5" />
                        <text x={bx + cell_w / 2.0} y={by + cell_h / 2.0 + 9.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">{b_vals[0]}</text>
                        <rect x={bx + cell_w + gap} y={by} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_AMBER} stroke-width="1.5" />
                        <text x={bx + cell_w + gap + cell_w / 2.0} y={by + cell_h / 2.0 + 9.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">{b_vals[1]}</text>
                        <rect x={bx + 2.0 * (cell_w + gap)} y={by} width={cell_w} height={cell_h} rx="10" fill="#1e293b" stroke={COLOR_AMBER} stroke-width="1.5" />
                        <text x={bx + 2.0 * (cell_w + gap) + cell_w / 2.0} y={by + cell_h / 2.0 + 9.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">{b_vals[2]}</text>
                    </g>
                    // expansion arrow
                    <g opacity={ghost_op}>
                        <line x1={bx + 1.5 * cell_w + gap} y1={by + cell_h + 8.0} x2={bx + 1.5 * cell_w + gap} y2={by + cell_h + 52.0} stroke={COLOR_AMBER} stroke-width="3" marker-end="url(#arrow-amber)" stroke-dasharray="6 4" />
                        <text x={bx + 1.5 * cell_w + gap + 14.0} y={by + cell_h + 40.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_AMBER}>"авто-розширення"</text>
                    </g>
                    // ghost broadcast row
                    <g opacity={ghost_op} transform={format!("translate(0 {:.1})", ghost_dy)}>
                        <rect x={bx} y={by + cell_h + 60.0} width={cell_w} height={cell_h} rx="10" fill="#0f172a" stroke={COLOR_AMBER} stroke-width="2" stroke-dasharray="8 5" opacity="0.9" />
                        <text x={bx + cell_w / 2.0} y={by + cell_h + 60.0 + cell_h / 2.0 + 9.0} font-family={FONT} font-size="24" font-weight="700" fill={COLOR_AMBER} text-anchor="middle" opacity="0.95">{b_vals[0]}</text>
                        <rect x={bx + cell_w + gap} y={by + cell_h + 60.0} width={cell_w} height={cell_h} rx="10" fill="#0f172a" stroke={COLOR_AMBER} stroke-width="2" stroke-dasharray="8 5" opacity="0.9" />
                        <text x={bx + cell_w + gap + cell_w / 2.0} y={by + cell_h + 60.0 + cell_h / 2.0 + 9.0} font-family={FONT} font-size="24" font-weight="700" fill={COLOR_AMBER} text-anchor="middle" opacity="0.95">{b_vals[1]}</text>
                        <rect x={bx + 2.0 * (cell_w + gap)} y={by + cell_h + 60.0} width={cell_w} height={cell_h} rx="10" fill="#0f172a" stroke={COLOR_AMBER} stroke-width="2" stroke-dasharray="8 5" opacity="0.9" />
                        <text x={bx + 2.0 * (cell_w + gap) + cell_w / 2.0} y={by + cell_h + 60.0 + cell_h / 2.0 + 9.0} font-family={FONT} font-size="24" font-weight="700" fill={COLOR_AMBER} text-anchor="middle" opacity="0.95">{b_vals[2]}</text>
                    </g>
                    <text x="920" y="620" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        "shape = [3] -> [1, 3] -> [2, 3]"
                    </text>
                    <text x="920" y="700" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">
                        "віртуальна копія: strides = 0"
                    </text>
                    <text x="920" y="726" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="middle">
                        "без дублювання пам'яті"
                    </text>
                </g>

                // ---- Equals / arrow to R ----
                <g opacity={g_alpha}>
                    <text x="1210" y="450" font-family={FONT} font-size="56" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"="</text>
                </g>

                // ---- Card R ----
                <g opacity={g_alpha}>
                    <rect x="1230" y="165" width="620" height="620" rx="18" fill={CARD_BG} stroke={COLOR_EMERALD} stroke-width="1.5" stroke-opacity={format!("{:.2}", 0.4 + 0.6 * rule_glow.min(1.0))} />
                    <rect x="1255" y="185" width="330" height="30" rx="8" fill="#1e293b" />
                    <text x="1270" y="205" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD} letter-spacing="1.0">
                        "РЕЗУЛЬТАТ R: (2, 3)"
                    </text>
                    // R cells 2x3 with staggered reveal (static SVG)
                    <g opacity={r_op[0]}>
                        <rect x={rx} y={ry} width={cell_w} height={cell_h} rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={rx + cell_w / 2.0} y={ry + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"11"</text>
                    </g>
                    <g opacity={r_op[1]}>
                        <rect x={rx + cell_w + gap} y={ry} width={cell_w} height={cell_h} rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={rx + cell_w + gap + cell_w / 2.0} y={ry + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"22"</text>
                    </g>
                    <g opacity={r_op[2]}>
                        <rect x={rx + 2.0 * (cell_w + gap)} y={ry} width={cell_w} height={cell_h} rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={rx + 2.0 * (cell_w + gap) + cell_w / 2.0} y={ry + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"33"</text>
                    </g>
                    <g opacity={r_op[3]}>
                        <rect x={rx} y={ry + cell_h + gap} width={cell_w} height={cell_h} rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={rx + cell_w / 2.0} y={ry + cell_h + gap + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"14"</text>
                    </g>
                    <g opacity={r_op[4]}>
                        <rect x={rx + cell_w + gap} y={ry + cell_h + gap} width={cell_w} height={cell_h} rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={rx + cell_w + gap + cell_w / 2.0} y={ry + cell_h + gap + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"25"</text>
                    </g>
                    <g opacity={r_op[5]}>
                        <rect x={rx + 2.0 * (cell_w + gap)} y={ry + cell_h + gap} width={cell_w} height={cell_h} rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={rx + 2.0 * (cell_w + gap) + cell_w / 2.0} y={ry + cell_h + gap + cell_h / 2.0 + 9.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"36"</text>
                    </g>
                    <text x="1540" y="560" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        "1+10=11 ... 6+30=36"
                    </text>
                    <text x="1540" y="700" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                        "[[11, 22, 33],"
                    </text>
                    <text x="1540" y="726" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                        " [14, 25, 36]]"
                    </text>
                </g>

                // ---- Bottom rule bar ----
                <g opacity={g_alpha}>
                    <rect x="70" y="810" width="1780" height="200" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="95" y="830" width="360" height="28" rx="8" fill="#1e293b" />
                    <text x="110" y="849" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_INDIGO} letter-spacing="1.0">
                        "ПРАВИЛА BROADCASTING (ВИРІВНЮВАННЯ ВПРАВО)"
                    </text>
                    <g transform="translate(110, 885)">
                        <text x="0" y="0" font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN}>"(2, 3)"</text>
                        <text x="110" y="0" font-family={FONT} font-size="20" font-weight="700" fill={COLOR_AMBER}>"+"</text>
                        <text x="140" y="0" font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN}>"(3,) → (1, 3) → (2, 3)"</text>
                        <text x="560" y="0" font-family={FONT} font-size="20" font-weight="700" fill={COLOR_EMERALD}>"= (2, 3) OK"</text>
                        <text x="0" y="34" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"розміри рівні — OK  |  один із розмірів = 1 — розтягнути  |  інакше — RuntimeError"</text>
                        <text x="0" y="62" font-family={FONT} font-size="15" fill={TEXT_DIM}>"(n,1)+(1,m) → (n,m)  |  (n,)+(n,m) → (n,m)  |  помилка, якщо k != m"</text>
                    </g>
                    <g transform="translate(1380, 880)">
                        <rect x="0" y="0" width="420" height="100" rx="12" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x="210" y="32" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"ПАМ'ЯТЬ: ZERO-COPY"</text>
                        <text x="210" y="58" font-family={FONT} font-size="13" fill={TEXT_MAIN} text-anchor="middle">"розширення через strides,"</text>
                        <text x="210" y="80" font-family={FONT} font-size="13" fill={TEXT_MAIN} text-anchor="middle">"без виділення VRAM"</text>
                    </g>
                </g>
            </svg>
        )
    }
}
