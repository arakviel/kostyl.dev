//! Linear regression training: y = 3x + 2 + noise, 100 epochs, lr=0.01.
//! Learned line rotates to true line, loss 5.57 -> 0.26, w -> 3, b -> 2.
//! 10s loop, dark theme.

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

#[inline]
fn lerp(a: f32, b: f32, p: f32) -> f32 {
    a + (b - a) * p
}

// Checkpoints from the article (epochs 0,20,40,60,80,100)
const EPS: [f32; 6] = [0.0, 20.0, 40.0, 60.0, 80.0, 100.0];
const LOSS: [f32; 6] = [8.5000, 5.5739, 2.4450, 1.0954, 0.5130, 0.2616];
const WW: [f32; 6] = [0.3932, 1.2730, 1.8558, 2.2420, 2.4979, 2.6677];
const BB: [f32; 6] = [-0.2148, 0.5673, 1.0752, 1.4048, 1.6186, 1.7571];

fn interp(table: &[f32; 6], ep: f32) -> f32 {
    for i in 0..5 {
        if ep <= EPS[i + 1] {
            let p = (ep - EPS[i]) / (EPS[i + 1] - EPS[i]);
            return lerp(table[i], table[i + 1], p);
        }
    }
    table[5]
}

// Deterministic pseudo-noise (LCG) in [-1, 1]
fn noise(i: usize) -> f32 {
    let mut s = (i as u64 * 1103515245 + 12345) & 0x7fffffff;
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    ((s % 2000) as f32 / 1000.0 - 1.0) * 0.55
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
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.0)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(6.8)..AudioTimestamp::Eof)
                .gain_db(0.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(8.2)..AudioTimestamp::Eof)
                .gain_db(1.0),
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

        // Training progress: epochs 0 -> 100 over t 1.0 -> 8.4
        let ep = clamp((t - 1.0) / 7.4, 0.0, 1.0) * 100.0;
        let loss = interp(&LOSS, ep);
        let w = interp(&WW, ep);
        let b = interp(&BB, ep);

        // Plot mapping: x in [-2.5, 2.5], y in [-7, 10]
        let px_lo = 150.0;
        let px_hi = 1150.0;
        let x_lo = -2.5;
        let x_hi = 2.5;
        let py_hi = 220.0;
        let py_lo = 700.0;
        let y_lo = -7.0;
        let y_hi = 10.0;
        let mx = |x: f32| px_lo + (x - x_lo) / (x_hi - x_lo) * (px_hi - px_lo);
        let my = |y: f32| py_lo - (y - y_lo) / (y_hi - y_lo) * (py_lo - py_hi);

        // Scatter points (60, deterministic) as one stroked path (round caps = dots).
        // NOTE: dynamic element markup does not compile in svgr!, but a path `d` string does.
        let mut dots = String::new();
        for i in 0..60 {
            let x = -2.2 + 4.4 * i as f32 / 59.0;
            let y = 3.0 * x + 2.0 + noise(i);
            dots.push_str(&format!("M {:.1} {:.1} h 0.1 ", mx(x), my(y)));
        }

        // True line y = 3x + 2 (dashed)
        let true_d = format!("M {:.1} {:.1} L {:.1} {:.1}", mx(x_lo), my(3.0 * x_lo + 2.0), mx(x_hi), my(3.0 * x_hi + 2.0));
        // Learned line y = w*x + b (clamped to plot)
        let ly0 = clamp(w * x_lo + b, y_lo, y_hi);
        let ly1 = clamp(w * x_hi + b, y_lo, y_hi);
        let learn_d = format!("M {:.1} {:.1} L {:.1} {:.1}", mx(x_lo), my(ly0), mx(x_hi), my(ly1));

        // Progress fractions
        let loss_frac = clamp(1.0 - (loss - 0.26) / (8.5 - 0.26), 0.0, 1.0);
        let w_frac = clamp((w - 0.39) / (3.0 - 0.39), 0.0, 1.0);
        let b_frac = clamp((b + 0.21) / (2.0 + 0.21), 0.0, 1.0);
        let done = if ep > 97.0 { 1.0 } else { 0.0 };

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
                    <rect x="600" y="24" width="720" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "НАВЧАННЯ З НУЛЯ: ЛІНІЙНА РЕГРЕСІЯ ЧЕРЕЗ AUTOGRAD"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "y = 3x + 2 + шум: пряма вчиться лягати на дані"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "100 прикладів, lr = 0.01, 100 епох: forward → backward → update → zero_grad"
                    </text>
                </g>

                // ---- Scatter + lines ----
                <g opacity={g_alpha}>
                    <rect x="70" y="155" width="1170" height="640" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <line x1={px_lo} y1={my(0.0)} x2={px_hi} y2={my(0.0)} stroke="#334155" stroke-width="1.5" />
                    <line x1={mx(0.0)} y1={py_hi} x2={mx(0.0)} y2={py_lo} stroke="#334155" stroke-width="1.5" stroke-dasharray="5 4" />
                    <text x={px_hi - 20.0} y={my(0.0) - 10.0} font-family={FONT} font-size="14" font-weight="700" fill={TEXT_DIM}>"x"</text>
                    <text x={mx(0.0) + 10.0} y={py_hi + 16.0} font-family={FONT} font-size="14" font-weight="700" fill={TEXT_DIM}>"y"</text>
                    <path d={dots} fill="none" stroke={COLOR_CYAN} stroke-width="10" stroke-linecap="round" opacity="0.55" />
                    <path d={true_d} fill="none" stroke={TEXT_DIM} stroke-width="2.5" stroke-dasharray="9 6" opacity="0.8" />
                    <text x={mx(2.0)} y={my(8.0) - 12.0} font-family={FONT} font-size="13" fill={TEXT_DIM}>"істинна: y = 3x + 2"</text>
                    <path d={learn_d} fill="none" stroke={COLOR_CYAN} stroke-width="4" />
                    <text x={mx(-2.2)} y={my(w * -2.2 + b) - 14.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN}>
                        {format!("навчена: y = {:.2}x + {:.2}", w, b)}
                    </text>
                    <rect x="90" y="720" width="340" height="56" rx="10" fill="#0f172a" stroke="#334155" stroke-width="1.5" />
                    <text x="260" y="745" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">"X @ w + b → MSELoss"</text>
                    <text x="260" y="765" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="middle">"батч 100×1, векторизовано"</text>
                </g>

                // ---- Stats ----
                <g opacity={g_alpha}>
                    <rect x="1270" y="155" width="580" height="640" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g transform="translate(1300, 210)">
                        <text x="0" y="0" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"ЕПОХА"</text>
                        <text x="0" y="46" font-family={FONT} font-size="40" font-weight="700" fill={COLOR_CYAN}>{format!("{:.0} / 100", ep)}</text>
                    </g>
                    <line x1="1300" y1="290" x2="1820" y2="290" stroke="#1e293b" stroke-width="1.5" />
                    <g transform="translate(1300, 320)">
                        <text x="0" y="0" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"MSE LOSS"</text>
                        <text x="0" y="46" font-family={FONT} font-size="40" font-weight="700" fill={COLOR_EMERALD}>{format!("{:.4}", loss)}</text>
                        <rect x="0" y="60" width="520" height="18" rx="9" fill="#1e293b" />
                        <rect x="0" y="60" width={520.0 * loss_frac} height="18" rx="9" fill={COLOR_EMERALD} opacity="0.9" />
                        <text x="0" y="104" font-family={FONT} font-size="13" fill={TEXT_MUTED}>"8.50 → 0.26 (у 33 рази менше)"</text>
                    </g>
                    <line x1="1300" y1="450" x2="1820" y2="450" stroke="#1e293b" stroke-width="1.5" />
                    <g transform="translate(1300, 480)">
                        <text x="0" y="0" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"ВАГА w → 3.0"</text>
                        <text x="0" y="42" font-family={FONT} font-size="32" font-weight="700" fill={TEXT_MAIN}>{format!("{:.4}", w)}</text>
                        <rect x="0" y="54" width="520" height="14" rx="7" fill="#1e293b" />
                        <rect x="0" y="54" width={520.0 * w_frac} height="14" rx="7" fill={COLOR_CYAN} opacity="0.9" />
                    </g>
                    <g transform="translate(1300, 600)">
                        <text x="0" y="0" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"ЗМІЩЕННЯ b → 2.0"</text>
                        <text x="0" y="42" font-family={FONT} font-size="32" font-weight="700" fill={TEXT_MAIN}>{format!("{:.4}", b)}</text>
                        <rect x="0" y="54" width="520" height="14" rx="7" fill="#1e293b" />
                        <rect x="0" y="54" width={520.0 * b_frac} height="14" rx="7" fill={COLOR_AMBER} opacity="0.9" />
                    </g>
                    <g opacity={done} transform="translate(1300, 700)">
                        <rect x="0" y="0" width="520" height="66" rx="12" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x="260" y="28" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"ЗБІГЛОСЯ ДО ІСТИННИХ"</text>
                        <text x="260" y="50" font-family={FONT} font-size="13" fill={TEXT_MAIN} text-anchor="middle">"w ≈ 2.67, b ≈ 1.76 (ще 100 епох — і 3.0/2.0)"</text>
                    </g>
                </g>

                // ---- Bottom loop ----
                <g opacity={g_alpha}>
                    <rect x="70" y="820" width="1780" height="190" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g transform="translate(110, 862)">
                        <text x="0" y="0" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">"ЦИКЛ НАВЧАННЯ — 4 КРОКИ КОЖНОЇ ЕПОХИ"</text>
                        <text x="0" y="40" font-family={FONT} font-size="19" fill={TEXT_MAIN}>"1) y_pred = X @ w + b (forward)   2) loss = MSE (скаляр)"</text>
                        <text x="0" y="72" font-family={FONT} font-size="19" fill={TEXT_MAIN}>"3) loss.backward() (grad)   4) w,b -= lr·grad під no_grad()"</text>
                        <text x="0" y="104" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_ROSE}>"5) w.grad.zero_() — інакше градієнти накопичаться і навчання зламається"</text>
                    </g>
                    <g transform="translate(1430, 850)">
                        <rect x="0" y="0" width="390" height="130" rx="12" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x="195" y="36" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"ЦЕ ВЖЕ НЕЙРОМЕРЕЖА"</text>
                        <text x="195" y="64" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"1 нейрон = лінійний шар"</text>
                        <text x="195" y="92" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"далі: nn.Module + оптимізатор"</text>
                    </g>
                </g>
            </svg>
        )
    }
}
