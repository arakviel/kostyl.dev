//! Multi-Layer Perceptron (MLP) Forward Pass visualization using fframes.
//!
//! Renders a 1920x1080 animated diagram of Forward Propagation:
//! 1. Input Layer (x1, x2, x3)
//! 2. Hidden Layer 1 (h1..h4) — Feature combination
//! 3. Hidden Layer 2 (h1'..h3') — High-level abstraction
//! 4. Output Layer (y1, y2) — Prediction / Classification
use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct MlpMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

// Light Theme Palette
const BG_COLOR: &str = "#FFFFFF";
const BG_DOT: &str = "#E2E8F0";
const CARD_BG: &str = "#FFFFFF";
const CARD_BORDER: &str = "#E2E8F0";

const TEXT_MAIN: &str = "#0F172A";
const TEXT_MUTED: &str = "#475569";

// Layer Colors (Light Theme)
const COLOR_BLUE_BG: &str = "#EFF6FF";
const COLOR_BLUE_BORDER: &str = "#3B82F6";
const COLOR_BLUE_TEXT: &str = "#1E40AF";

const COLOR_AMBER_BG: &str = "#FEF3C7";
const COLOR_AMBER_BORDER: &str = "#F59E0B";
const COLOR_AMBER_ACTIVE: &str = "#D97706";
const COLOR_AMBER_TEXT: &str = "#92400E";

const COLOR_TEAL_BG: &str = "#CCFBF1";
const COLOR_TEAL_BORDER: &str = "#0D9488";
const COLOR_TEAL_ACTIVE: &str = "#0F766E";
const COLOR_TEAL_TEXT: &str = "#115E59";

const COLOR_GREEN_BG: &str = "#DCFCE7";
const COLOR_GREEN_BORDER: &str = "#10B981";
const COLOR_GREEN_ACTIVE: &str = "#059669";
const COLOR_GREEN_TEXT: &str = "#065F46";

const LINE_PASSIVE: &str = "#E2E8F0";

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

pub struct MlpVideo<'a> {
    pub media: &'a MlpMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> MlpVideo<'a> {
    pub fn new(media: &'a MlpMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for MlpVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("MlpVideo").finish()
    }
}

impl fframes::Video for MlpVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(255, 255, 255);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.2)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(2.6)..AudioTimestamp::Eof).gain_db(-1.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(3.4)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(4.8)..AudioTimestamp::Eof).gain_db(-1.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(5.8)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(7.2)..AudioTimestamp::Eof).gain_db(0.0),
        ])
    }

    fn render_frame<'a>(&'a self, frame: Frame, _ctx: &FFramesContext<'a, '_>) -> Svgr<'a> {
        let t = frame.seconds();

        // Layer X Coordinates
        let x_in = 320.0_f32;
        let x_h1 = 730.0_f32;
        let x_h2 = 1140.0_f32;
        let x_out = 1550.0_f32;

        // Layer Node Y Centers
        let y_in = [380.0_f32, 520.0, 660.0];
        let y_h1 = [310.0_f32, 450.0, 590.0, 730.0];
        let y_h2 = [380.0_f32, 520.0, 660.0];
        let y_out = [450.0_f32, 590.0];

        // Radii
        let r_in = 38.0_f32;
        let r_h1 = 36.0_f32;
        let r_h2 = 36.0_f32;
        let r_out = 40.0_f32;

        // Intro fade in (0.0s -> 0.8s)
        let intro_alpha = ease_out_cubic(clamp(t / 0.8, 0.0, 1.0));

        // Seamless loop fade out at end (9.2s -> 10.0s)
        let loop_reset = if t >= 9.2 {
            1.0 - ease_in_out(clamp((t - 9.2) / 0.8, 0.0, 1.0))
        } else {
            1.0
        };

        // Phase 1 -> 2: Signal Input -> Hidden 1 (1.2s -> 2.6s)
        let sig1_t = clamp((t - 1.2) / 1.4, 0.0, 1.0);
        let sig1_p = ease_out_cubic(sig1_t);
        let sig1_active = if t >= 1.2 && t < 3.2 { loop_reset } else { 0.0 };

        // Hidden 1 Activation (2.6s -> 9.4s)
        let h1_act_t = clamp((t - 2.6) / 0.6, 0.0, 1.0);
        let h1_alpha = ease_out_cubic(h1_act_t) * loop_reset;
        let h1_activated = t >= 2.6 && t < 9.5;

        // Phase 2 -> 3: Signal Hidden 1 -> Hidden 2 (3.4s -> 4.8s)
        let sig2_t = clamp((t - 3.4) / 1.4, 0.0, 1.0);
        let sig2_p = ease_out_cubic(sig2_t);
        let sig2_active = if t >= 3.4 && t < 5.4 { loop_reset } else { 0.0 };

        // Hidden 2 Activation (4.8s -> 9.4s)
        let h2_act_t = clamp((t - 4.8) / 0.6, 0.0, 1.0);
        let h2_alpha = ease_out_cubic(h2_act_t) * loop_reset;
        let h2_activated = t >= 4.8 && t < 9.5;

        // Phase 3 -> 4: Signal Hidden 2 -> Output (5.8s -> 7.2s)
        let sig3_t = clamp((t - 5.8) / 1.4, 0.0, 1.0);
        let sig3_p = ease_out_cubic(sig3_t);
        let sig3_active = if t >= 5.8 && t < 7.8 { loop_reset } else { 0.0 };

        // Output Activation (7.2s -> 9.4s)
        let out_act_t = clamp((t - 7.2) / 0.6, 0.0, 1.0);
        let out_alpha = ease_out_cubic(out_act_t) * loop_reset;
        let out_activated = t >= 7.2 && t < 9.6;

        // Determine current phase for status pill
        let current_phase = if t < 1.2 {
            1
        } else if t < 3.4 {
            2
        } else if t < 5.8 {
            3
        } else if t < 8.2 {
            4
        } else {
            5
        };

        let (phase_title, phase_desc) = match current_phase {
            1 => ("ФАЗА 1: ВХІДНІ ДАНІ (INPUT LAYER)", "Вхідні значення x = [+1.2, +0.5, -0.8] готові до подачі в мережу"),
            2 => ("ФАЗА 2: ПРИХОВАНИЙ ШАР 1 (HIDDEN LAYER 1)", "Обчислення z^[1] = W^[1]x + b^[1] та активація нейронів: a^[1] = ReLU(z^[1])"),
            3 => ("ФАЗА 3: ПРИХОВАНИЙ ШАР 2 (HIDDEN LAYER 2)", "Високорівневі комбінації ознак: a^[2] = ReLU(W^[2]a^[1] + b^[2])"),
            4 => ("ФАЗА 4: ВИХІДНИЙ ШАР (OUTPUT LAYER)", "Softmax обчислює ймовірність: Клас 1 = 98.4%, Клас 0 = 1.6%"),
            _ => ("ФАЗА 5: ПЕРЕДБАЧЕННЯ СФОРМОВАНО", "Повний прямий прохід (Forward Pass) успішно завершено"),
        };

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <radialGradient id="soft-wash" cx="0.5" cy="0.5" r="0.6">
                        <stop offset="0%" stop-color="#F1F5F9" stop-opacity="0.8" />
                        <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.4" />
                        <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
                    </radialGradient>

                    <pattern id="dot-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="1.3" fill={BG_DOT} />
                    </pattern>

                    <filter id="shadow-card" x="-10%" y="-10%" width="120%" height="120%">
                        <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.06" />
                    </filter>
                    <filter id="shadow-node" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.08" />
                    </filter>
                </defs>

                // Background
                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH as f32 / 2.0} cy={540.0} r="700" fill="url(#soft-wash)" />

                // Top Header Section
                <g opacity={intro_alpha}>
                    <rect x={(WIDTH as f32 / 2.0) - 180.0} y="32" width="360" height="34" rx="17" fill="#EFF6FF" stroke="#3B82F6" stroke-width="1.5" />
                    <text x={WIDTH as f32 / 2.0} y="54" font-family={FONT} font-size="13" font-weight="700" fill="#2563EB" text-anchor="middle" letter-spacing="1.2">
                        "БАГАТОШАРОВИЙ ПЕРСЕПТРОН (MLP)"
                    </text>

                    <text x={WIDTH as f32 / 2.0} y="104" font-family={FONT} font-size="32" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Архітектура мережі & Прямий прохід сигналу (Forward Pass)"
                    </text>

                    <text x={WIDTH as f32 / 2.0} y="138" font-family={FONT} font-size="17" fill={TEXT_MUTED} text-anchor="middle">
                        "Вхідний шар → Приховані шари (нелінійні комбінації ознак) → Фінальне передбачення"
                    </text>
                </g>

                // Layer Vertical Headers (Labels above columns)
                <g opacity={intro_alpha}>
                    // Input Layer Label
                    <rect x={x_in - 85.0} y="250" width="170" height="42" rx="10" fill={COLOR_BLUE_BG} stroke={COLOR_BLUE_BORDER} stroke-width="1.5" filter="url(#shadow-node)" />
                    <text x={x_in} y="276" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_BLUE_TEXT} text-anchor="middle">
                        "Вхідний шар (x)"
                    </text>

                    // Hidden Layer 1 Label
                    <rect x={x_h1 - 95.0} y="210" width="190" height="42" rx="10" fill={COLOR_AMBER_BG} stroke={COLOR_AMBER_BORDER} stroke-width="1.5" filter="url(#shadow-node)" />
                    <text x={x_h1} y="236" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_AMBER_TEXT} text-anchor="middle">
                        "Прихований шар 1"
                    </text>

                    // Hidden Layer 2 Label
                    <rect x={x_h2 - 95.0} y="250" width="190" height="42" rx="10" fill={COLOR_TEAL_BG} stroke={COLOR_TEAL_BORDER} stroke-width="1.5" filter="url(#shadow-node)" />
                    <text x={x_h2} y="276" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_TEAL_TEXT} text-anchor="middle">
                        "Прихований шар 2"
                    </text>

                    // Output Layer Label
                    <rect x={x_out - 85.0} y="320" width="170" height="42" rx="10" fill={COLOR_GREEN_BG} stroke={COLOR_GREEN_BORDER} stroke-width="1.5" filter="url(#shadow-node)" />
                    <text x={x_out} y="346" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_GREEN_TEXT} text-anchor="middle">
                        "Вихідний шар (ŷ)"
                    </text>
                </g>

                // Static Connection Lines (Passive)
                <g opacity={intro_alpha * 0.7}>
                    // Connections: In -> H1
                    {
                        (0..3).flat_map(|i| {
                            (0..4).map(move |j| {
                                fframes::svgr!(
                                    <line x1={x_in} y1={y_in[i]} x2={x_h1} y2={y_h1[j]} stroke={LINE_PASSIVE} stroke-width="2.0" />
                                )
                            })
                        }).collect::<Vec<_>>()
                    }

                    // Connections: H1 -> H2
                    {
                        (0..4).flat_map(|i| {
                            (0..3).map(move |j| {
                                fframes::svgr!(
                                    <line x1={x_h1} y1={y_h1[i]} x2={x_h2} y2={y_h2[j]} stroke={LINE_PASSIVE} stroke-width="2.0" />
                                )
                            })
                        }).collect::<Vec<_>>()
                    }

                    // Connections: H2 -> Out
                    {
                        (0..3).flat_map(|i| {
                            (0..2).map(move |j| {
                                fframes::svgr!(
                                    <line x1={x_h2} y1={y_h2[i]} x2={x_out} y2={y_out[j]} stroke={LINE_PASSIVE} stroke-width="2.0" />
                                )
                            })
                        }).collect::<Vec<_>>()
                    }
                </g>

                // Dynamic Pulses on Connections: In -> H1
                {
                    if sig1_active > 0.0 {
                        fframes::svgr!(
                            <g opacity={sig1_active}>
                                {
                                    (0..3).flat_map(|i| {
                                        (0..4).map(move |j| {
                                            let cur_x = x_in + (x_h1 - x_in) * sig1_p;
                                            let cur_y = y_in[i] + (y_h1[j] - y_in[i]) * sig1_p;
                                            fframes::svgr!(
                                                <g>
                                                    <line x1={x_in} y1={y_in[i]} x2={cur_x} y2={cur_y} stroke="#93C5FD" stroke-width="2.5" />
                                                    <circle cx={cur_x} cy={cur_y} r="6" fill="#3B82F6" />
                                                    <circle cx={cur_x} cy={cur_y} r="12" fill="#60A5FA" opacity="0.3" />
                                                </g>
                                            )
                                        })
                                    }).collect::<Vec<_>>()
                                }
                            </g>
                        )
                    } else {
                        fframes::svgr!(<g></g>)
                    }
                }

                // Dynamic Pulses on Connections: H1 -> H2
                {
                    if sig2_active > 0.0 {
                        fframes::svgr!(
                            <g opacity={sig2_active}>
                                {
                                    (0..4).flat_map(|i| {
                                        (0..3).map(move |j| {
                                            let cur_x = x_h1 + (x_h2 - x_h1) * sig2_p;
                                            let cur_y = y_h1[i] + (y_h2[j] - y_h1[i]) * sig2_p;
                                            fframes::svgr!(
                                                <g>
                                                    <line x1={x_h1} y1={y_h1[i]} x2={cur_x} y2={cur_y} stroke="#FCD34D" stroke-width="2.5" />
                                                    <circle cx={cur_x} cy={cur_y} r="6" fill="#F59E0B" />
                                                    <circle cx={cur_x} cy={cur_y} r="12" fill="#FBBF24" opacity="0.3" />
                                                </g>
                                            )
                                        })
                                    }).collect::<Vec<_>>()
                                }
                            </g>
                        )
                    } else {
                        fframes::svgr!(<g></g>)
                    }
                }

                // Dynamic Pulses on Connections: H2 -> Out
                {
                    if sig3_active > 0.0 {
                        fframes::svgr!(
                            <g opacity={sig3_active}>
                                {
                                    (0..3).flat_map(|i| {
                                        (0..2).map(move |j| {
                                            let cur_x = x_h2 + (x_out - x_h2) * sig3_p;
                                            let cur_y = y_h2[i] + (y_out[j] - y_h2[i]) * sig3_p;
                                            fframes::svgr!(
                                                <g>
                                                    <line x1={x_h2} y1={y_h2[i]} x2={cur_x} y2={cur_y} stroke="#5EEAD4" stroke-width="2.5" />
                                                    <circle cx={cur_x} cy={cur_y} r="6" fill="#0D9488" />
                                                    <circle cx={cur_x} cy={cur_y} r="12" fill="#14B8A6" opacity="0.3" />
                                                </g>
                                            )
                                        })
                                    }).collect::<Vec<_>>()
                                }
                            </g>
                        )
                    } else {
                        fframes::svgr!(<g></g>)
                    }
                }

                // Input Layer Nodes
                <g opacity={intro_alpha}>
                    {
                        let in_labels = ["x1 = +1.2", "x2 = +0.5", "x3 = -0.8"];
                        let in_names = ["x1", "x2", "x3"];
                        (0..3).map(|i| {
                            let cy = y_in[i];
                            fframes::svgr!(
                                <g filter="url(#shadow-node)">
                                    <circle cx={x_in} cy={cy} r={r_in} fill={COLOR_BLUE_BG} stroke={COLOR_BLUE_BORDER} stroke-width="3" />
                                    <circle cx={x_in} cy={cy} r={r_in - 5.0} fill="#FFFFFF" opacity="0.6" />
                                    <text x={x_in} y={cy + 6.0} font-family={FONT} font-size="18" font-weight="700" fill={COLOR_BLUE_TEXT} text-anchor="middle">
                                        {in_names[i]}
                                    </text>
                                    <text x={x_in - 55.0} y={cy + 5.0} font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED} text-anchor="end">
                                        {in_labels[i]}
                                    </text>
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }
                </g>

                // Hidden Layer 1 Nodes
                <g opacity={intro_alpha}>
                    {
                        let h1_names = ["h1", "h2", "h3", "h4"];
                        let h1_vals = ["a=1.4", "a=0.9", "a=0.0", "a=1.8"];
                        (0..4).map(|i| {
                            let cy = y_h1[i];
                            let border_color = if h1_activated { COLOR_AMBER_ACTIVE } else { COLOR_AMBER_BORDER };
                            let border_w = if h1_activated { "3.5" } else { "2.5" };
                            let glow_opacity = if h1_activated { h1_alpha * 0.4 } else { 0.0 };

                            fframes::svgr!(
                                <g filter="url(#shadow-node)">
                                    <circle cx={x_h1} cy={cy} r={r_h1 + 10.0} fill="#F59E0B" opacity={glow_opacity} />
                                    <circle cx={x_h1} cy={cy} r={r_h1} fill={COLOR_AMBER_BG} stroke={border_color} stroke-width={border_w} />
                                    <circle cx={x_h1} cy={cy} r={r_h1 - 5.0} fill="#FFFFFF" opacity="0.6" />
                                    <text x={x_h1} y={cy + 6.0} font-family={FONT} font-size="17" font-weight="700" fill={COLOR_AMBER_TEXT} text-anchor="middle">
                                        {h1_names[i]}
                                    </text>
                                    {
                                        if h1_activated {
                                            fframes::svgr!(
                                                <text x={x_h1} y={cy + r_h1 + 18.0} font-family={FONT} font-size="12" font-weight="700" fill={COLOR_AMBER_ACTIVE} text-anchor="middle" opacity={h1_alpha}>
                                                    {h1_vals[i]}
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }
                </g>

                // Hidden Layer 2 Nodes
                <g opacity={intro_alpha}>
                    {
                        let h2_names = ["h1'", "h2'", "h3'"];
                        let h2_vals = ["a=2.1", "a=0.4", "a=1.5"];
                        (0..3).map(|i| {
                            let cy = y_h2[i];
                            let border_color = if h2_activated { COLOR_TEAL_ACTIVE } else { COLOR_TEAL_BORDER };
                            let border_w = if h2_activated { "3.5" } else { "2.5" };
                            let glow_opacity = if h2_activated { h2_alpha * 0.4 } else { 0.0 };

                            fframes::svgr!(
                                <g filter="url(#shadow-node)">
                                    <circle cx={x_h2} cy={cy} r={r_h2 + 10.0} fill="#0D9488" opacity={glow_opacity} />
                                    <circle cx={x_h2} cy={cy} r={r_h2} fill={COLOR_TEAL_BG} stroke={border_color} stroke-width={border_w} />
                                    <circle cx={x_h2} cy={cy} r={r_h2 - 5.0} fill="#FFFFFF" opacity="0.6" />
                                    <text x={x_h2} y={cy + 6.0} font-family={FONT} font-size="17" font-weight="700" fill={COLOR_TEAL_TEXT} text-anchor="middle">
                                        {h2_names[i]}
                                    </text>
                                    {
                                        if h2_activated {
                                            fframes::svgr!(
                                                <text x={x_h2} y={cy + r_h2 + 18.0} font-family={FONT} font-size="12" font-weight="700" fill={COLOR_TEAL_ACTIVE} text-anchor="middle" opacity={h2_alpha}>
                                                    {h2_vals[i]}
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }
                </g>

                // Output Layer Nodes
                <g opacity={intro_alpha}>
                    {
                        let out_names = ["y1", "y0"];
                        let out_labels = ["Клас 1: 98.4%", "Клас 0: 1.6%"];
                        (0..2).map(|i| {
                            let cy = y_out[i];
                            let is_winner = i == 0;
                            let border_color = if out_activated && is_winner { COLOR_GREEN_ACTIVE } else { COLOR_GREEN_BORDER };
                            let border_w = if out_activated && is_winner { "4.0" } else { "2.5" };
                            let glow_opacity = if out_activated && is_winner { out_alpha * 0.5 } else { 0.0 };

                            fframes::svgr!(
                                <g filter="url(#shadow-node)">
                                    <circle cx={x_out} cy={cy} r={r_out + 12.0} fill="#10B981" opacity={glow_opacity} />
                                    <circle cx={x_out} cy={cy} r={r_out} fill={COLOR_GREEN_BG} stroke={border_color} stroke-width={border_w} />
                                    <circle cx={x_out} cy={cy} r={r_out - 6.0} fill="#FFFFFF" opacity="0.6" />
                                    <text x={x_out} y={cy + 7.0} font-family={FONT} font-size="20" font-weight="700" fill={COLOR_GREEN_TEXT} text-anchor="middle">
                                        {out_names[i]}
                                    </text>
                                    <text x={x_out + 60.0} y={cy + 7.0} font-family={FONT} font-size="16" font-weight="700" fill={if is_winner && out_activated { COLOR_GREEN_ACTIVE } else { TEXT_MUTED }} text-anchor="start">
                                        {out_labels[i]}
                                    </text>
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }
                </g>

                // Winner Badge (when output activated)
                {
                    if out_activated {
                        fframes::svgr!(
                            <g opacity={out_alpha} filter="url(#shadow-card)">
                                <rect x={x_out + 55.0} y="380" width="230" height="40" rx="8" fill="#ECFDF5" stroke="#10B981" stroke-width="1.5" />
                                <text x={x_out + 170.0} y="405" font-family={FONT} font-size="14" font-weight="700" fill="#047857" text-anchor="middle">
                                    "ПЕРЕДБАЧЕННЯ: КЛАС 1"
                                </text>
                            </g>
                        )
                    } else {
                        fframes::svgr!(<g></g>)
                    }
                }

                // Bottom Status Card & Phase Progress
                <g opacity={intro_alpha}>
                    <rect x="220" y="930" width="1480" height="96" rx="14" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" filter="url(#shadow-card)" />

                    // Phase Pills
                    <g>
                        // Pill 1
                        <rect x="250" y="946" width="320" height="28" rx="6" fill={if current_phase == 1 { "#EFF6FF" } else { "#F8FAFC" }} stroke={if current_phase == 1 { "#3B82F6" } else { "#E2E8F0" }} stroke-width="1.5" />
                        <text x="410" y="965" font-family={FONT} font-size="12" font-weight="700" fill={if current_phase == 1 { "#1D4ED8" } else { "#64748B" }} text-anchor="middle">
                            "1. Вхідний шар (Input)"
                        </text>

                        // Pill 2
                        <rect x="600" y="946" width="320" height="28" rx="6" fill={if current_phase == 2 { "#FEF3C7" } else { "#F8FAFC" }} stroke={if current_phase == 2 { "#F59E0B" } else { "#E2E8F0" }} stroke-width="1.5" />
                        <text x="760" y="965" font-family={FONT} font-size="12" font-weight="700" fill={if current_phase == 2 { "#B45309" } else { "#64748B" }} text-anchor="middle">
                            "2. Прихований шар 1"
                        </text>

                        // Pill 3
                        <rect x="950" y="946" width="320" height="28" rx="6" fill={if current_phase == 3 { "#CCFBF1" } else { "#F8FAFC" }} stroke={if current_phase == 3 { "#0D9488" } else { "#E2E8F0" }} stroke-width="1.5" />
                        <text x="1110" y="965" font-family={FONT} font-size="12" font-weight="700" fill={if current_phase == 3 { "#0F766E" } else { "#64748B" }} text-anchor="middle">
                            "3. Прихований шар 2"
                        </text>

                        // Pill 4
                        <rect x="1300" y="946" width="320" height="28" rx="6" fill={if current_phase >= 4 { "#DCFCE7" } else { "#F8FAFC" }} stroke={if current_phase >= 4 { "#10B981" } else { "#E2E8F0" }} stroke-width="1.5" />
                        <text x="1460" y="965" font-family={FONT} font-size="12" font-weight="700" fill={if current_phase >= 4 { "#047857" } else { "#64748B" }} text-anchor="middle">
                            "4. Вихідний шар (Output)"
                        </text>
                    </g>

                    // Phase description line
                    <text x="250" y="1005" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN}>
                        {phase_title}
                    </text>
                    <text x="650" y="1005" font-family={FONT} font-size="14" fill={TEXT_MUTED}>
                        {phase_desc}
                    </text>
                </g>
            </svg>
        )
    }
}
