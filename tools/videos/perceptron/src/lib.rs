//! Perceptron Forward Pass visualization using fframes.
//!
//! Renders a 1920x1080 animated diagram of the Frank Rosenblatt Perceptron:
//! 1. Inputs (x1, x2) and Bias (b)
//! 2. Synaptic Weights (w1, w2, w0) and signal transmission
//! 3. Weighted Sum node (z = ∑ wi*xi + b)
//! 4. Step Activation function (σ(z) = Heaviside(z))
//! 5. Final Output classification (ŷ ∈ {0, 1})
use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct PerceptronMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

// Palette
const BG_COLOR: &str = "#070b14";
const CARD_BG: &str = "#0f172a";
const CARD_BORDER: &str = "#1e293b";
const TEXT_MAIN: &str = "#f8fafc";
const TEXT_MUTED: &str = "#94a3b8";
const TEXT_DIM: &str = "#64748b";

const COLOR_CYAN: &str = "#38bdf8";
const COLOR_INDIGO: &str = "#818cf8";
const COLOR_AMBER: &str = "#f59e0b";
const COLOR_EMERALD: &str = "#10b981";
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

pub struct PerceptronVideo<'a> {
    pub media: &'a PerceptronMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> PerceptronVideo<'a> {
    pub fn new(media: &'a PerceptronMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for PerceptronVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PerceptronVideo").finish()
    }
}

impl fframes::Video for PerceptronVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(2.3)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(6.9)..AudioTimestamp::Eof).gain_db(0.0),
        ])
    }

    fn render_frame<'a>(&'a self, frame: Frame, _ctx: &FFramesContext<'a, '_>) -> Svgr<'a> {
        let t = frame.seconds();

        // Geometry Coordinates
        // Inputs (Left Column)
        let in_x = 280.0_f32;
        let y_x1 = 330.0_f32;
        let y_x2 = 530.0_f32;
        let y_b  = 730.0_f32;
        let r_in = 46.0_f32;

        // Core Perceptron Node (Center)
        let core_cx = 960.0_f32;
        let core_cy = 530.0_f32;
        let core_r = 190.0_f32;

        // Core Entry Points for lines
        let entry_x = core_cx - core_r + 15.0;
        let entry_y1 = core_cy - 70.0;
        let entry_y2 = core_cy;
        let entry_y3 = core_cy + 70.0;

        // Output Node (Right Column)
        let out_cx = 1620.0_f32;
        let out_cy = 530.0_f32;
        let r_out = 56.0_f32;
        let exit_x = core_cx + core_r - 10.0;

        // Timings & Easing
        let intro_alpha = ease_out_cubic(clamp(t / 1.0, 0.0, 1.0));

        // Signal Travel (Phase 2): 2.2s -> 4.4s
        let sig_t = clamp((t - 2.2) / 2.0, 0.0, 1.0);
        let sig_p = ease_in_out(sig_t);
        let sig_active = if t >= 2.2 && t <= 4.8 { 1.0 } else { 0.0 };

        let sig1_x = in_x + (entry_x - in_x) * sig_p;
        let sig1_y = y_x1 + (entry_y1 - y_x1) * sig_p;

        let sig2_x = in_x + (entry_x - in_x) * sig_p;
        let sig2_y = y_x2 + (entry_y2 - y_x2) * sig_p;

        let sig3_x = in_x + (entry_x - in_x) * sig_p;
        let sig3_y = y_b  + (entry_y3 - y_b) * sig_p;

        // Summation Glow (Phase 3): 4.4s -> 6.8s
        let sum_t = clamp((t - 4.4) / 1.0, 0.0, 1.0);
        let sum_alpha = ease_out_cubic(sum_t);

        // Core Transfer Line
        let trans_t = clamp((t - 5.6) / 1.0, 0.0, 1.0);
        let trans_p = ease_in_out(trans_t);
        let trans_x = (core_cx - 80.0) + 160.0 * trans_p;

        // Smooth Loop Relaxation (Phase 5 ending): 9.3s -> 10.0s
        let loop_reset = if t >= 9.3 {
            1.0 - ease_in_out(clamp((t - 9.3) / 0.7, 0.0, 1.0))
        } else {
            1.0
        };

        // Activation Trigger (Phase 4): 6.9s -> 9.4s
        let act_t = clamp((t - 6.9) / 0.8, 0.0, 1.0);
        let act_alpha = ease_out_cubic(act_t) * loop_reset;
        let is_activated = t >= 6.9 && t < 9.7;

        // Shockwave Ripple
        let rip_t = clamp((t - 6.9) / 1.4, 0.0, 1.0);
        let rip_r = r_out + 90.0 * rip_t;
        let rip_opacity = (1.0 - rip_t) * 0.85;

        // Output beam travel
        let beam_t = clamp((t - 6.9) / 0.5, 0.0, 1.0);
        let beam_p = ease_out_cubic(beam_t);
        let beam_head_x = exit_x + (out_cx - r_out - exit_x) * beam_p;
        let beam_opacity = if is_activated { loop_reset } else { 0.0 };

        // Phase Step Badge highlight
        let current_phase = if t < 2.2 {
            1
        } else if t < 4.4 {
            2
        } else if t < 6.9 {
            3
        } else if t < 8.8 {
            4
        } else {
            5
        };

        let (phase_title, phase_desc) = match current_phase {
            1 => ("ФАЗА 1: ІНІЦІАЛІЗАЦІЯ ОЗНАК ТА ВАГ", "Вхідні значення x = [1.5, 0.8] та зсув b = 1.0 підготовлені до обробки"),
            2 => ("ФАЗА 2: СИНАПТИЧНА ПЕРЕДАЧА СИГНАЛУ", "Обчислення добутків: x1·w1 = +1.20, x2·w2 = +0.40 та зсуву b·w0 = -1.00"),
            3 => ("ФАЗА 3: ЗВАЖЕНА СУМА (СУМАТОР Σ)", "Лінійна комбінація: z = (1.5×0.8) + (0.8×0.5) - 1.0 = +0.60"),
            4 => ("ФАЗА 4: ПОРОГОВА ФУНКЦІЯ АКТИВАЦІЇ", "Оскільки z = +0.60 ≥ 0, Heaviside Step видає сигнал збудження: ŷ = 1"),
            _ => ("ФАЗА 5: РЕЗУЛЬТАТ ПЕРЕДБАЧЕННЯ", "Персептрон успішно класифікував об'єкт як Клас 1 (ŷ = 1)"),
        };

        let out_color = if is_activated { COLOR_EMERALD } else { TEXT_DIM };

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <radialGradient id="bg-glow" cx="0.5" cy="0.45" r="0.6">
                        <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.45" />
                        <stop offset="60%" stop-color="#0b1329" stop-opacity="0.15" />
                        <stop offset="100%" stop-color={BG_COLOR} stop-opacity="0" />
                    </radialGradient>

                    <radialGradient id="core-glow" cx="0.5" cy="0.5" r="0.5">
                        <stop offset="0%" stop-color="#0284c7" stop-opacity={format!("{:.2}", 0.15 + sum_alpha * 0.25)} />
                        <stop offset="100%" stop-color="#0f172a" stop-opacity="0" />
                    </radialGradient>

                    <radialGradient id="act-glow" cx="0.5" cy="0.5" r="0.5">
                        <stop offset="0%" stop-color="#10b981" stop-opacity={format!("{:.2}", act_alpha * 0.6)} />
                        <stop offset="100%" stop-color="#10b981" stop-opacity="0" />
                    </radialGradient>

                    <pattern id="dot-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="1.2" fill="#334155" opacity="0.3" />
                    </pattern>
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={core_cx} cy={core_cy} r="650" fill="url(#bg-glow)" />

                <g opacity={intro_alpha}>
                    <rect x={core_cx - 180.0} y="38" width="360" height="34" rx="17" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x={core_cx} y="60" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "ПЕРСЕПТРОН РОЗЕНБЛАТТА (1957)"
                    </text>

                    <text x={core_cx} y="112" font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Анатомія штучного нейрона & Прямий прохід (Forward Pass)"
                    </text>

                    <text x={core_cx} y="148" font-family={FONT} font-size="18" fill={TEXT_MUTED} text-anchor="middle">
                        "Лінійна зважена сума z = ∑ wi·xi + b та нелінійне порогове перетворення ŷ = σ(z)"
                    </text>
                </g>

                <g opacity={intro_alpha}>
                    <line x1={in_x + r_in} y1={y_x1} x2={entry_x} y2={entry_y1} stroke="#1e293b" stroke-width="4" stroke-linecap="round" />
                    <line x1={in_x + r_in} y1={y_x2} x2={entry_x} y2={entry_y2} stroke="#1e293b" stroke-width="4" stroke-linecap="round" />
                    <line x1={in_x + r_in} y1={y_b}  x2={entry_x} y2={entry_y3} stroke="#1e293b" stroke-width="4" stroke-linecap="round" />
                    <line x1={exit_x} y1={out_cy} x2={out_cx - r_out} y2={out_cy} stroke="#1e293b" stroke-width="5" stroke-linecap="round" />
                </g>

                {
                    if sig_active > 0.0 {
                        fframes::svgr!(
                            <g>
                                <line x1={in_x + r_in} y1={y_x1} x2={sig1_x} y2={sig1_y} stroke={COLOR_CYAN} stroke-width="4" stroke-linecap="round" opacity="0.9" />
                                <circle cx={sig1_x} cy={sig1_y} r="9" fill={COLOR_CYAN} />
                                <circle cx={sig1_x} cy={sig1_y} r="16" fill={COLOR_CYAN} opacity="0.4" />

                                <line x1={in_x + r_in} y1={y_x2} x2={sig2_x} y2={sig2_y} stroke={COLOR_INDIGO} stroke-width="4" stroke-linecap="round" opacity="0.9" />
                                <circle cx={sig2_x} cy={sig2_y} r="9" fill={COLOR_INDIGO} />
                                <circle cx={sig2_x} cy={sig2_y} r="16" fill={COLOR_INDIGO} opacity="0.4" />

                                <line x1={in_x + r_in} y1={y_b} x2={sig3_x} y2={sig3_y} stroke={COLOR_AMBER} stroke-width="4" stroke-linecap="round" opacity="0.9" />
                                <circle cx={sig3_x} cy={sig3_y} r="9" fill={COLOR_AMBER} />
                                <circle cx={sig3_x} cy={sig3_y} r="16" fill={COLOR_AMBER} opacity="0.4" />
                            </g>
                        )
                    } else {
                        fframes::svgr!(<g></g>)
                    }
                }

                {
                    if is_activated && beam_opacity > 0.01 {
                        fframes::svgr!(
                            <g opacity={format!("{:.2}", beam_opacity)}>
                                <line x1={exit_x} y1={out_cy} x2={beam_head_x} y2={out_cy} stroke={COLOR_EMERALD} stroke-width="6" stroke-linecap="round" />
                                <circle cx={beam_head_x} cy={out_cy} r="11" fill={COLOR_EMERALD} />
                                <circle cx={beam_head_x} cy={out_cy} r="22" fill={COLOR_EMERALD} opacity="0.5" />
                            </g>
                        )
                    } else {
                        fframes::svgr!(<g></g>)
                    }
                }

                <g opacity={intro_alpha}>
                    <g transform="translate(490, 360)">
                        <rect x="-85" y="-28" width="170" height="56" rx="10" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        <text x="0" y="-6" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                            "w1 = +0.80"
                        </text>
                        <text x="0" y="16" font-family={FONT} font-size="12" fill={TEXT_MUTED} text-anchor="middle">
                            "x1·w1 = +1.20"
                        </text>
                    </g>

                    <g transform="translate(490, 530)">
                        <rect x="-85" y="-28" width="170" height="56" rx="10" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        <text x="0" y="-6" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_INDIGO} text-anchor="middle">
                            "w2 = +0.50"
                        </text>
                        <text x="0" y="16" font-family={FONT} font-size="12" fill={TEXT_MUTED} text-anchor="middle">
                            "x2·w2 = +0.40"
                        </text>
                    </g>

                    <g transform="translate(490, 700)">
                        <rect x="-85" y="-28" width="170" height="56" rx="10" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        <text x="0" y="-6" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">
                            "w0 (b) = -1.00"
                        </text>
                        <text x="0" y="16" font-family={FONT} font-size="12" fill={TEXT_MUTED} text-anchor="middle">
                            "b = -1.00"
                        </text>
                    </g>
                </g>

                <g opacity={intro_alpha}>
                    <g>
                        <circle cx={in_x} cy={y_x1} r={r_in + 8.0} fill={COLOR_CYAN} opacity="0.1" />
                        <circle cx={in_x} cy={y_x1} r={r_in} fill={CARD_BG} stroke={COLOR_CYAN} stroke-width="3" />
                        <text x={in_x} y={y_x1 - 4.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                            "x1"
                        </text>
                        <text x={in_x} y={y_x1 + 18.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                            "= 1.5"
                        </text>
                        <text x={in_x - r_in - 16.0} y={y_x1 + 6.0} font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MUTED} text-anchor="end">
                            "Ознака 1"
                        </text>
                    </g>

                    <g>
                        <circle cx={in_x} cy={y_x2} r={r_in + 8.0} fill={COLOR_INDIGO} opacity="0.1" />
                        <circle cx={in_x} cy={y_x2} r={r_in} fill={CARD_BG} stroke={COLOR_INDIGO} stroke-width="3" />
                        <text x={in_x} y={y_x2 - 4.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                            "x2"
                        </text>
                        <text x={in_x} y={y_x2 + 18.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_INDIGO} text-anchor="middle">
                            "= 0.8"
                        </text>
                        <text x={in_x - r_in - 16.0} y={y_x2 + 6.0} font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MUTED} text-anchor="end">
                            "Ознака 2"
                        </text>
                    </g>

                    <g>
                        <circle cx={in_x} cy={y_b} r={r_in + 8.0} fill={COLOR_AMBER} opacity="0.1" />
                        <circle cx={in_x} cy={y_b} r={r_in} fill={CARD_BG} stroke={COLOR_AMBER} stroke-width="3" />
                        <text x={in_x} y={y_b - 4.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                            "+1"
                        </text>
                        <text x={in_x} y={y_b + 18.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">
                            "Зсув (b)"
                        </text>
                        <text x={in_x - r_in - 16.0} y={y_b + 6.0} font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MUTED} text-anchor="end">
                            "Постійний вхід"
                        </text>
                    </g>
                </g>

                <g opacity={intro_alpha}>
                    <circle cx={core_cx} cy={core_cy} r={core_r + 14.0} fill="url(#core-glow)" />
                    <circle cx={core_cx} cy={core_cy} r={core_r} fill={CARD_BG} stroke="#334155" stroke-width="3" />

                    <line x1={core_cx} y1={core_cy - core_r + 15.0} x2={core_cx} y2={core_cy + core_r - 15.0} stroke="#475569" stroke-width="2" stroke-dasharray="6,6" />

                    {
                        if t >= 5.6 && t <= 7.2 {
                            fframes::svgr!(
                                <g>
                                    <line x1={core_cx - 70.0} y1={core_cy} x2={trans_x} y2={core_cy} stroke={COLOR_CYAN} stroke-width="3" stroke-dasharray="4,4" />
                                    <circle cx={trans_x} cy={core_cy} r="6" fill={COLOR_CYAN} />
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    <g transform={format!("translate({}, {})", core_cx - 95.0, core_cy)}>
                        <text x="0" y="-120" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1">
                            "СУМАТОР"
                        </text>

                        <text x="0" y="-55" font-family={FONT} font-size="52" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                            "Σ"
                        </text>

                        <text x="0" y="-22" font-family={FONT} font-size="15" fill={TEXT_MUTED} text-anchor="middle">
                            "z = ∑ wi·xi + b"
                        </text>

                        <rect x="-80" y="10" width="160" height="74" rx="10" fill="#1e293b" stroke={if t >= 4.4 && t < 9.7 { COLOR_CYAN } else { "#334155" }} stroke-width="1.5" />
                        <text x="0" y="38" font-family={FONT} font-size="13" fill={TEXT_MUTED} text-anchor="middle">
                            "1.2 + 0.4 - 1.0"
                        </text>
                        <text x="0" y="68" font-family={FONT} font-size="24" font-weight="700" fill={if t >= 4.4 && t < 9.7 { COLOR_CYAN } else { TEXT_DIM }} text-anchor="middle">
                            "z = +0.60"
                        </text>
                    </g>

                    <g transform={format!("translate({}, {})", core_cx + 95.0, core_cy)}>
                        <text x="0" y="-120" font-family={FONT} font-size="13" font-weight="700" fill={if is_activated { COLOR_EMERALD } else { TEXT_MUTED }} text-anchor="middle" letter-spacing="1">
                            "АКТИВАЦІЯ"
                        </text>

                        <text x="0" y="-95" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                            "σ(z) = Step(z)"
                        </text>

                        <g transform="translate(0, -10)">
                            <line x1="-65" y1="35" x2="65" y2="35" stroke="#475569" stroke-width="1.5" />
                            <line x1="0" y1="45" x2="0" y2="-40" stroke="#475569" stroke-width="1.5" />

                            <text x="60" y="50" font-family={FONT} font-size="11" fill={TEXT_MUTED} text-anchor="middle">"z"</text>
                            <text x="12" y="-32" font-family={FONT} font-size="11" fill={TEXT_MUTED} text-anchor="start">"1"</text>
                            <text x="-8" y="48" font-family={FONT} font-size="11" fill={TEXT_MUTED} text-anchor="end">"0"</text>

                            <line x1="-60" y1="35" x2="0" y2="35" stroke={COLOR_ROSE} stroke-width="3" stroke-linecap="round" />
                            <line x1="0" y1="35" x2="0" y2="-25" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" />
                            <line x1="0" y1="-25" x2="60" y2="-25" stroke={COLOR_EMERALD} stroke-width="3.5" stroke-linecap="round" />

                            {
                                if is_activated {
                                    fframes::svgr!(
                                        <g>
                                            <circle cx="26" cy="-25" r="9" fill={COLOR_EMERALD} />
                                            <circle cx="26" cy="-25" r="16" fill={COLOR_EMERALD} opacity="0.4" />
                                            <text x="32" y="-34" font-family={FONT} font-size="11" font-weight="700" fill={COLOR_EMERALD}>
                                                "+0.60 ≥ 0"
                                            </text>
                                        </g>
                                    )
                                } else {
                                    fframes::svgr!(<g></g>)
                                }
                            }
                        </g>

                        <rect x="-70" y="56" width="140" height="28" rx="6" fill="#1e293b" stroke={if is_activated { COLOR_EMERALD } else { "#334155" }} stroke-width="1" />
                        <text x="0" y="75" font-family={FONT} font-size="12" font-weight="700" fill={if is_activated { COLOR_EMERALD } else { TEXT_MUTED }} text-anchor="middle">
                            "якщо z ≥ 0 -> 1"
                        </text>
                    </g>
                </g>

                <g opacity={intro_alpha}>
                    {
                        if is_activated && rip_opacity > 0.01 {
                            fframes::svgr!(
                                <circle cx={out_cx} cy={out_cy} r={rip_r} fill="none" stroke={COLOR_EMERALD} stroke-width="3" opacity={format!("{:.2}", rip_opacity)} />
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    <circle cx={out_cx} cy={out_cy} r={r_out + 18.0} fill="url(#act-glow)" />
                    <circle cx={out_cx} cy={out_cy} r={r_out} fill={CARD_BG} stroke={out_color} stroke-width="4" />

                    <text x={out_cx} y={out_cy - 6.0} font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "ŷ"
                    </text>
                    <text x={out_cx} y={out_cy + 24.0} font-family={FONT} font-size="24" font-weight="700" fill={out_color} text-anchor="middle">
                        {if is_activated { "= 1" } else { "= ?" }}
                    </text>

                    <text x={out_cx} y={out_cy + r_out + 28.0} font-family={FONT} font-size="18" font-weight="700" fill={out_color} text-anchor="middle">
                        {if is_activated { "КЛАС 1 (АКТИВОВАНО)" } else { "ОЧІКУВАННЯ ОБЧИСЛЕННЯ" }}
                    </text>
                    <text x={out_cx} y={out_cy + r_out + 52.0} font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        "Позитивний прогноз"
                    </text>
                </g>

                <g opacity={intro_alpha} transform="translate(190, 890)">
                    <rect x="0" y="0" width="1540" height="135" rx="16" fill="#0f172a" stroke="#1e293b" stroke-width="1.5" />

                    <g transform="translate(40, 32)">
                        <rect x="0" y="0" width="270" height="34" rx="8" fill={if current_phase == 1 { "#0369a1" } else { "#1e293b" }} />
                        <text x="135" y="22" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 1 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "1. Вхідні дані & Ваги"
                        </text>

                        <rect x="295" y="0" width="270" height="34" rx="8" fill={if current_phase == 2 { "#4338ca" } else { "#1e293b" }} />
                        <text x="430" y="22" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 2 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "2. Передача сигналів"
                        </text>

                        <rect x="590" y="0" width="270" height="34" rx="8" fill={if current_phase == 3 { "#0284c7" } else { "#1e293b" }} />
                        <text x="725" y="22" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 3 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "3. Зважена сума Σ"
                        </text>

                        <rect x="885" y="0" width="270" height="34" rx="8" fill={if current_phase == 4 { "#059669" } else { "#1e293b" }} />
                        <text x="1020" y="22" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 4 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "4. Поріг & Активація"
                        </text>

                        <rect x="1180" y="0" width="270" height="34" rx="8" fill={if current_phase == 5 { "#047857" } else { "#1e293b" }} />
                        <text x="1315" y="22" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 5 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "5. Вихідний клас ŷ"
                        </text>
                    </g>

                    <text x="50" y="94" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_CYAN}>
                        {phase_title}
                    </text>
                    <text x="50" y="118" font-family={FONT} font-size="15" fill={TEXT_MUTED}>
                        {phase_desc}
                    </text>

                    <text x="1490" y="108" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_DIM} text-anchor="end">
                        {format!("Час: {:.1}c / 10.0c  •  Кадр {}", t, frame.index)}
                    </text>
                </g>
            </svg>
        )
    }
}
