//! Backpropagation Cycle visualization using fframes.
//!
//! Visualizes the 4 essential steps of neural network training:
//! 1. Forward Pass: data moves from input to output.
//! 2. Loss Computation: predicted output vs actual target.
//! 3. Backward Pass: gradients propagate backwards via the Chain Rule.
//! 4. Weight Update: optimizer nudges weights opposite to gradients to reduce error.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct BackpropMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

// Light Theme Palette
const BG_COLOR: &str = "#FFFFFF";
const BG_DOT: &str = "#E2E8F0";
const CARD_BG: &str = "#FFFFFF";
const CARD_BORDER: &str = "#E2E8F0";

const TEXT_MAIN: &str = "#0F172A";
const TEXT_MUTED: &str = "#64748B";

const COLOR_BLUE: &str = "#2563EB";
const COLOR_PURPLE: &str = "#7C3AED";
const COLOR_RED: &str = "#DC2626";
const COLOR_GREEN: &str = "#059669";
const COLOR_AMBER: &str = "#D97706";

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

pub struct BackpropVideo<'a> {
    pub media: &'a BackpropMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> BackpropVideo<'a> {
    pub fn new(media: &'a BackpropMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for BackpropVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("BackpropVideo").finish()
    }
}

impl fframes::Video for BackpropVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(255, 255, 255);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(0.5)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(4.8)..AudioTimestamp::Eof).gain_db(0.0),
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
        let master_opacity = intro_alpha * loop_reset;

        // Phase Timing:
        // Phase 1: Forward Pass (0.0s - 2.5s)
        // Phase 2: Loss Computation (2.5s - 4.5s)
        // Phase 3: Backward Pass (4.5s - 7.5s)
        // Phase 4: Weight Update (7.5s - 9.2s)
        let forward_progress = clamp(t / 2.2, 0.0, 1.0);
        let is_loss_active = t >= 2.5 && t < 7.5;
        let backward_progress = clamp((t - 4.5) / 2.6, 0.0, 1.0);
        let is_update_active = t >= 7.5;

        // Node positions in the network
        // Input Layer: 2 nodes
        let in_x = 280.0_f32;
        let in_nodes = [(in_x, 400.0_f32), (in_x, 580.0_f32)];

        // Hidden Layer: 3 nodes
        let hid_x = 760.0_f32;
        let hid_nodes = [(hid_x, 340.0_f32), (hid_x, 490.0_f32), (hid_x, 640.0_f32)];

        // Output Node: 1 node
        let out_x = 1240.0_f32;
        let out_node = (out_x, 490.0_f32);

        // Target / Loss Node
        let loss_x = 1620.0_f32;
        let loss_node = (loss_x, 490.0_f32);

        // Active phase banner title and colors
        let (phase_num, phase_title, phase_color, phase_badge_bg, phase_border) = if t < 2.5 {
            ("ЕТАП 1 / 4", "Прямий прохід (Forward Pass): вхід x -> обчислення передбачення y_pred", COLOR_BLUE, "#EFF6FF", "#BFDBFE")
        } else if t < 4.5 {
            ("ЕТАП 2 / 4", "Функція втрат (Loss): порівняння передбачення y_pred = 0.85 з ціллю y = 0.00", COLOR_RED, "#FEF2F2", "#FECACA")
        } else if t < 7.5 {
            ("ЕТАП 3 / 4", "Зворотний прохід (Backpropagation): розрахунок градієнтів dL/dw через Chain Rule", COLOR_PURPLE, "#FAF5FF", "#E9D5FF")
        } else {
            ("ЕТАП 4 / 4", "Оновлення ваг (Weight Update): w_new = w_old - learning_rate * dL/dw", COLOR_GREEN, "#ECFDF5", "#A7F3D0")
        };

        // Forward pulse packet x coordinates
        let fwd_wave_x = in_x + (out_x - in_x) * forward_progress;
        // Backward pulse packet x coordinates
        let bwd_wave_x = out_x - (out_x - in_x) * backward_progress;

        fframes::svgr!(
            <svg viewBox="0 0 1920 1080" width="1920" height="1080">
                <defs>
                    <filter id="shadow-card" x="-4%" y="-4%" width="108%" height="112%">
                        <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.06" />
                    </filter>
                    <filter id="shadow-node" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.10" />
                    </filter>
                    <filter id="glow-loss" x="-30%" y="-30%" width="160%" height="160%">
                        <feDropShadow dx="0" dy="0" stdDeviation="14" flood-color="#DC2626" flood-opacity="0.45" />
                    </filter>
                    <pattern id="dot-grid" width="30" height="30" patternUnits="userSpaceOnUse">
                        <circle cx="2" cy="2" r="1.2" fill={BG_DOT} />
                    </pattern>
                </defs>

                // Canvas Background
                <rect width="1920" height="1080" fill={BG_COLOR} />
                <rect width="1920" height="1080" fill="url(#dot-grid)" opacity="0.8" />

                <g opacity={master_opacity}>
                    // ================= HEADER =================
                    <text x="80" y="75" font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN}>
                        "Повний цикл навчання нейромережі: від Forward до Backpropagation"
                    </text>
                    <text x="80" y="112" font-family={FONT} font-size="18" font-weight="500" fill={TEXT_MUTED}>
                        "Прямий сигнал генерує результат • Функція втрат вимірює помилку • Градієнти оновлюють параметри"
                    </text>

                    // Top Phase Banner
                    <g filter="url(#shadow-card)">
                        <rect x="80" y="145" width="1760" height="64" rx="14" fill={phase_badge_bg} stroke={phase_border} stroke-width="1.5" />
                        <rect x="100" y="159" width="140" height="36" rx="8" fill={phase_color} />
                        <text x="170" y="183" font-family={FONT} font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">
                            {phase_num}
                        </text>
                        <text x="260" y="186" font-family={FONT} font-size="20" font-weight="700" fill={phase_color}>
                            {phase_title}
                        </text>
                    </g>

                    // ================= MAIN COMPUTATION CANVAS =================
                    <g filter="url(#shadow-card)">
                        <rect x="80" y="235" width="1760" height="680" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />

                        // Layer Headers
                        <text x={in_x} y="280" font-family={FONT} font-size="18" font-weight="700" fill={TEXT_MUTED} text-anchor="middle">
                            "Вхідний шар (X)"
                        </text>
                        <text x={hid_x} y="280" font-family={FONT} font-size="18" font-weight="700" fill={TEXT_MUTED} text-anchor="middle">
                            "Прихований шар (Hidden ReLU)"
                        </text>
                        <text x={out_x} y="280" font-family={FONT} font-size="18" font-weight="700" fill={TEXT_MUTED} text-anchor="middle">
                            "Вихідний шар (Output)"
                        </text>
                        <text x={loss_x} y="280" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_RED} text-anchor="middle">
                            "Функція втрат (MSE Loss)"
                        </text>

                        // Synapses: Input -> Hidden
                        {
                            in_nodes.iter().enumerate().flat_map(|(i, &p1)| {
                                hid_nodes.iter().enumerate().map(move |(j, &p2)| {
                                    let is_fwd_active = t < 2.5 && fwd_wave_x >= p1.0 && fwd_wave_x <= p2.0;
                                    let is_bwd_active = t >= 4.5 && t < 7.5 && bwd_wave_x >= p1.0 && bwd_wave_x <= p2.0;
                                    let stroke = if is_bwd_active {
                                        COLOR_PURPLE
                                    } else if is_fwd_active {
                                        COLOR_BLUE
                                    } else if is_update_active {
                                        COLOR_GREEN
                                    } else {
                                        "#CBD5E1"
                                    };
                                    let stroke_w = if is_bwd_active || is_fwd_active || is_update_active { "3.5" } else { "1.8" };
                                    fframes::svgr!(
                                        <line x1={p1.0} y1={p1.1} x2={p2.0} y2={p2.1} stroke={stroke} stroke-width={stroke_w} />
                                    )
                                })
                            }).collect::<Vec<_>>()
                        }

                        // Synapses: Hidden -> Output
                        {
                            hid_nodes.iter().enumerate().map(|(j, &p2)| {
                                let is_fwd_active = t < 2.5 && fwd_wave_x >= p2.0 && fwd_wave_x <= out_node.0;
                                let is_bwd_active = t >= 4.5 && t < 7.5 && bwd_wave_x >= p2.0 && bwd_wave_x <= out_node.0;
                                let stroke = if is_bwd_active {
                                    COLOR_PURPLE
                                } else if is_fwd_active {
                                    COLOR_BLUE
                                } else if is_update_active {
                                    COLOR_GREEN
                                } else {
                                    "#CBD5E1"
                                };
                                let stroke_w = if is_bwd_active || is_fwd_active || is_update_active { "4.0" } else { "2.0" };
                                fframes::svgr!(
                                    <line x1={p2.0} y1={p2.1} x2={out_node.0} y2={out_node.1} stroke={stroke} stroke-width={stroke_w} />
                                )
                            }).collect::<Vec<_>>()
                        }

                        // Connection Output -> Loss
                        <line x1={out_node.0} y1={out_node.1} x2={loss_node.0} y2={loss_node.1} stroke={if is_loss_active { COLOR_RED } else { "#CBD5E1" }} stroke-width="3.5" stroke-dasharray="6 4" />

                        // Backward Gradient Arrows Indicator (when in phase 3)
                        {
                            if t >= 4.5 && t < 7.5 {
                                fframes::svgr!(
                                    <g>
                                        // Arrow Output -> Hidden
                                        <line x1="1160" y1="410" x2="840" y2="410" stroke={COLOR_PURPLE} stroke-width="3" stroke-dasharray="8 6" />
                                        <polygon points="840,410 852,404 852,416" fill={COLOR_PURPLE} />
                                        <rect x="940" y="375" width="120" height="26" rx="6" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1.0" />
                                        <text x="1000" y="393" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_PURPLE} text-anchor="middle">
                                            "dL/dh = dL/dy * W2"
                                        </text>

                                        // Arrow Hidden -> Input
                                        <line x1="680" y1="410" x2="360" y2="410" stroke={COLOR_PURPLE} stroke-width="3" stroke-dasharray="8 6" />
                                        <polygon points="360,410 372,404 372,416" fill={COLOR_PURPLE} />
                                        <rect x="460" y="375" width="120" height="26" rx="6" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1.0" />
                                        <text x="520" y="393" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_PURPLE} text-anchor="middle">
                                            "dL/dw1 = dL/dh * x"
                                        </text>
                                    </g>
                                )
                            } else {
                                fframes::svgr!(<g></g>)
                            }
                        }

                        // Weight Update Badges (Phase 4)
                        {
                            if is_update_active {
                                fframes::svgr!(
                                    <g>
                                        <rect x="440" y="520" width="160" height="34" rx="8" fill="#ECFDF5" stroke="#6EE7B7" stroke-width="1.5" />
                                        <text x="520" y="542" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                                            "W1 <- W1 - lr * grad"
                                        </text>

                                        <rect x="920" y="520" width="160" height="34" rx="8" fill="#ECFDF5" stroke="#6EE7B7" stroke-width="1.5" />
                                        <text x="1000" y="542" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                                            "W2 <- W2 - lr * grad"
                                        </text>
                                    </g>
                                )
                            } else {
                                fframes::svgr!(<g></g>)
                            }
                        }

                        // INPUT NODES
                        {
                            in_nodes.iter().enumerate().map(|(i, &p)| {
                                fframes::svgr!(
                                    <g filter="url(#shadow-node)">
                                        <circle cx={p.0} cy={p.1} r="38" fill="#F8FAFC" stroke={COLOR_BLUE} stroke-width="3.5" />
                                        <text x={p.0} y={p.1 + 6.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                                            {format!("x{}", i + 1)}
                                        </text>
                                        <text x={p.0} y={p.1 + 60.0} font-family={FONT} font-size="14" font-weight="600" fill={TEXT_MUTED} text-anchor="middle">
                                            {if i == 0 { "= 1.0" } else { "= 0.5" }}
                                        </text>
                                    </g>
                                )
                            }).collect::<Vec<_>>()
                        }

                        // HIDDEN NODES
                        {
                            hid_nodes.iter().enumerate().map(|(j, &p)| {
                                let is_active = t < 2.5 && fwd_wave_x >= p.0;
                                let node_fill = if is_active { "#DBEAFE" } else { "#F8FAFC" };
                                fframes::svgr!(
                                    <g filter="url(#shadow-node)">
                                        <circle cx={p.0} cy={p.1} r="42" fill={node_fill} stroke={if is_active { COLOR_BLUE } else { "#0F172A" }} stroke-width="3.5" />
                                        <text x={p.0} y={p.1 + 6.0} font-family={FONT} font-size="19" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                                            {format!("h{}", j + 1)}
                                        </text>
                                        <text x={p.0} y={p.1 + 65.0} font-family={FONT} font-size="13" font-weight="600" fill={TEXT_MUTED} text-anchor="middle">
                                            "ReLU(z)"
                                        </text>
                                    </g>
                                )
                            }).collect::<Vec<_>>()
                        }

                        // OUTPUT NODE
                        <g filter="url(#shadow-node)">
                            <circle cx={out_node.0} cy={out_node.1} r="48" fill={if t < 2.5 { "#EFF6FF" } else { "#FFFFFF" }} stroke={COLOR_PURPLE} stroke-width="4.0" />
                            <text x={out_node.0} y={out_node.1 - 4.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                                "y_pred"
                            </text>
                            <text x={out_node.0} y={out_node.1 + 20.0} font-family={FONT} font-size="16" font-weight="700" fill={COLOR_PURPLE} text-anchor="middle">
                                "= 0.85"
                            </text>
                            <text x={out_node.0} y={out_node.1 + 75.0} font-family={FONT} font-size="14" font-weight="600" fill={TEXT_MUTED} text-anchor="middle">
                                "Вихід мережі"
                            </text>
                        </g>

                        // LOSS NODE
                        <g filter={if is_loss_active { "url(#glow-loss)" } else { "url(#shadow-node)" }}>
                            <rect x={loss_node.0 - 110.0} y={loss_node.1 - 70.0} width="220" height="140" rx="16" fill={if is_loss_active { "#FEF2F2" } else { "#F8FAFC" }} stroke={COLOR_RED} stroke-width="3.0" />
                            <text x={loss_node.0} y={loss_node.1 - 32.0} font-family={FONT} font-size="16" font-weight="700" fill={COLOR_RED} text-anchor="middle">
                                "Ціль: y_true = 0.0"
                            </text>
                            <text x={loss_node.0} y={loss_node.1 + 4.0} font-family={FONT} font-size="22" font-weight="700" fill={COLOR_RED} text-anchor="middle">
                                "Loss = 0.722"
                            </text>
                            <text x={loss_node.0} y={loss_node.1 + 38.0} font-family={FONT} font-size="13" font-weight="600" fill="#991B1B" text-anchor="middle">
                                "MSE: (0.85 - 0.0)^2"
                            </text>
                            <text x={loss_node.0} y={loss_node.1 + 100.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_RED} text-anchor="middle">
                                "Джерело градієнта"
                            </text>
                        </g>

                        // Bottom Metrics / Live Status Card
                        <rect x="120" y="780" width="1680" height="100" rx="14" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5" />
                        <text x="160" y="822" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                            "Поточний статус циклу навчання:"
                        </text>
                        <text x="160" y="855" font-family={FONT} font-size="18" font-weight="600" fill={phase_color}>
                            {if t < 2.5 {
                                "-> Пряме розповсюдження: обчислення z = Wx + b та активацій ReLU на кожному шарі..."
                            } else if t < 4.5 {
                                "[!] Виявлено велику помилку прогнозу (Loss = 0.722). Необхідна термінова корекція ваг!"
                            } else if t < 7.5 {
                                "<- Зворотний прохід: ланцюгове правило dL/dw = (dL/dy) * (dy/dz) * (dz/dw) передає імпульс назад..."
                            } else {
                                "[OK] Крок оптимізатора виконано! Ваги скориговано на -lr * grad, прогнозована помилка наступної епохи спаде до 0.21"
                            }}
                        </text>
                    </g>

                    // ================= FOOTER =================
                    <circle cx="100" cy="980" r="8" fill={COLOR_BLUE} />
                    <text x="120" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Прямий сигнал (Forward)"
                    </text>

                    <circle cx="360" cy="980" r="8" fill={COLOR_RED} />
                    <text x="380" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Помилка (Loss L)"
                    </text>

                    <circle cx="560" cy="980" r="8" fill={COLOR_PURPLE} />
                    <text x="580" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Градієнти (Backpropagation)"
                    </text>

                    <circle cx="850" cy="980" r="8" fill={COLOR_GREEN} />
                    <text x="870" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Оновлення ваг (Optimizer step)"
                    </text>

                    <text x="1840" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MUTED} text-anchor="end">
                        "kostyl.dev • Інженерний практикум з нейромереж"
                    </text>

                    // Bottom Progress Line
                    <line x1="80" y1="1020" x2={80.0 + 1760.0 * (t / 10.0)} y2="1020" stroke={phase_color} stroke-width="4.0" />
                </g>
            </svg>
        )
    }
}
