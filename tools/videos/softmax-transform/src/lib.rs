//! Softmax Transformation visualization using fframes.
//!
//! Visualizes how arbitrary logits z are exponentiated into positive numbers
//! and normalized into a probability distribution summing strictly to 1.0 (100%).

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct SoftmaxMedia, "media");

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
const COLOR_GREEN: &str = "#059669";

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

pub struct SoftmaxVideo<'a> {
    pub media: &'a SoftmaxMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> SoftmaxVideo<'a> {
    pub fn new(media: &'a SoftmaxMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for SoftmaxVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("SoftmaxVideo").finish()
    }
}

impl fframes::Video for SoftmaxVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(255, 255, 255);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.8)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(4.5)..AudioTimestamp::Eof).gain_db(0.0),
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

        // Stage progress
        // Stage 1: Logits reveal (0.0s - 1.5s)
        let p1_ease = ease_out_cubic(clamp((t - 0.2) / 1.0, 0.0, 1.0));

        // Stage 2: Exponential calc (1.8s - 3.2s)
        let p2_ease = ease_out_cubic(clamp((t - 1.8) / 1.0, 0.0, 1.0));

        // Stage 3: Normalized Probabilities (3.8s - 5.5s)
        let p3_ease = ease_out_cubic(clamp((t - 3.8) / 1.0, 0.0, 1.0));

        // Winner pulse glow
        let winner_pulse = if t > 5.2 && t < 9.0 {
            0.5 + 0.5 * ((t - 5.2) * 6.0).sin()
        } else {
            0.0
        };

        // Item data
        let row_ys = [340.0, 480.0, 620.0];
        let class_names = ["1. Кішка (Cat)", "2. Собака (Dog)", "3. Птах (Bird)"];
        let logits = [2.00_f32, 1.00_f32, 0.10_f32];
        let exps = [7.389_f32, 2.718_f32, 1.105_f32];
        let probs = [0.6590_f32, 0.2424_f32, 0.0986_f32];
        let max_bar_w = 320.0_f32;

        fframes::svgr!(
            <svg viewBox="0 0 1920 1080" width="1920" height="1080">
                <defs>
                    <filter id="shadow-card" x="-4%" y="-4%" width="108%" height="112%">
                        <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.06" />
                    </filter>
                    <filter id="glow-winner" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#059669" flood-opacity="0.35" />
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
                    <text x="80" y="80" font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN}>
                        "Як працює Softmax: від сирих оцінок до ймовірностей"
                    </text>
                    <text x="80" y="118" font-family={FONT} font-size="18" font-weight="500" fill={TEXT_MUTED}>
                        "Крок 1: Логіти z -> Крок 2: Експоненціювання exp(z) -> Крок 3: Нормалізація (сума рівно 100%)"
                    </text>

                    // Badge top right
                    <rect x="1390" y="55" width="450" height="48" rx="24" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5" />
                    <text x="1615" y="85" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                        "Вихідний шар для багатокласової класифікації"
                    </text>

                    // ================= PANEL 1: LOGITS =================
                    <g filter="url(#shadow-card)" opacity={p1_ease}>
                        <rect x="80" y="170" width="480" height="730" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        
                        <rect x="110" y="200" width="420" height="56" rx="10" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1.5" />
                        <text x="130" y="235" font-family={FONT} font-size="20" font-weight="700" fill={COLOR_BLUE}>
                            "1. Сирі виходи (Логіти z)"
                        </text>

                        <text x="110" y="285" font-family={FONT} font-size="15" font-weight="500" fill={TEXT_MUTED}>
                            "Необмежені числа після W · x + b:"
                        </text>

                        {
                            (0..3).map(|i| {
                                let y = row_ys[i];
                                let z = logits[i];
                                let cur_bar_w = (z / 2.0 * max_bar_w * p1_ease).max(12.0);
                                fframes::svgr!(
                                    <g>
                                        <text x="110" y={y} font-family={FONT} font-size="18" font-weight="700" fill={TEXT_MAIN}>
                                            {class_names[i]}
                                        </text>
                                        <text x="490" y={y} font-family={FONT} font-size="18" font-weight="700" fill={COLOR_BLUE} text-anchor="end">
                                            {format!("z = {:.2}", z)}
                                        </text>
                                        <rect x="110" y={y + 12.0} width={max_bar_w} height="22" rx="6" fill="#F1F5F9" stroke="#E2E8F0" stroke-width="1.0" />
                                        <rect x="110" y={y + 12.0} width={cur_bar_w} height="22" rx="6" fill="#3B82F6" />
                                    </g>
                                )
                            }).collect::<Vec<_>>()
                        }

                        <rect x="105" y="720" width="430" height="80" rx="10" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.0" />
                        <text x="125" y="750" font-family={FONT} font-size="14" font-weight="700" fill="#DC2626">
                            "[!] Недолік: це не ймовірності!"
                        </text>
                        <text x="125" y="775" font-family={FONT} font-size="13" font-weight="500" fill="#991B1B">
                            "Сума 2.0 + 1.0 + 0.1 = 3.1 != 1.0, можуть бути < 0."
                        </text>
                    </g>

                    // ================= ARROW 1 -> 2 =================
                    <g opacity={p2_ease}>
                        <line x1="575" y1="500" x2="635" y2="500" stroke={COLOR_PURPLE} stroke-width="4.0" stroke-dasharray="6 4" />
                        <polygon points="635,500 623,492 623,508" fill={COLOR_PURPLE} />
                        <rect x="580" y="445" width="55" height="30" rx="6" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1.0" />
                        <text x="607" y="466" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_PURPLE} text-anchor="middle">
                            "exp(z)"
                        </text>
                    </g>

                    // ================= PANEL 2: EXPONENTIAL =================
                    <g filter="url(#shadow-card)" opacity={p2_ease}>
                        <rect x="650" y="170" width="540" height="730" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        
                        <rect x="680" y="200" width="480" height="56" rx="10" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1.5" />
                        <text x="700" y="235" font-family={FONT} font-size="20" font-weight="700" fill={COLOR_PURPLE}>
                            "2. Експоненціювання: e^z"
                        </text>

                        <text x="680" y="285" font-family={FONT} font-size="15" font-weight="500" fill={TEXT_MUTED}>
                            "Робить числа строго > 0 і підсилює сильні бали:"
                        </text>

                        {
                            (0..3).map(|i| {
                                let y = row_ys[i];
                                let z = logits[i];
                                let exp_val = exps[i];
                                let exp_bar_w = (exp_val / 7.389 * 380.0 * p2_ease).max(12.0);
                                fframes::svgr!(
                                    <g>
                                        <text x="680" y={y} font-family={FONT} font-size="18" font-weight="700" fill={TEXT_MAIN}>
                                            {format!("exp({:.2})", z)}
                                        </text>
                                        <text x="1150" y={y} font-family={FONT} font-size="20" font-weight="700" fill={COLOR_PURPLE} text-anchor="end">
                                            {format!("= {:.3}", exp_val)}
                                        </text>
                                        <rect x="680" y={y + 12.0} width="380" height="22" rx="6" fill="#F1F5F9" stroke="#E2E8F0" stroke-width="1.0" />
                                        <rect x="680" y={y + 12.0} width={exp_bar_w} height="22" rx="6" fill="#A855F7" />
                                    </g>
                                )
                            }).collect::<Vec<_>>()
                        }

                        <rect x="675" y="710" width="490" height="100" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5" />
                        <text x="695" y="740" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN}>
                            "Сума всіх експонент (Знаменник sum):"
                        </text>
                        <text x="695" y="775" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_PURPLE}>
                            "sum = 7.389 + 2.718 + 1.105 = 11.212"
                        </text>
                    </g>

                    // ================= ARROW 2 -> 3 =================
                    <g opacity={p3_ease}>
                        <line x1="1205" y1="500" x2="1265" y2="500" stroke={COLOR_GREEN} stroke-width="4.0" stroke-dasharray="6 4" />
                        <polygon points="1265,500 1253,492 1253,508" fill={COLOR_GREEN} />
                        <rect x="1210" y="445" width="55" height="30" rx="6" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.0" />
                        <text x="1237" y="466" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                            "/ sum"
                        </text>
                    </g>

                    // ================= PANEL 3: NORMALIZED PROBABILITIES =================
                    <g filter="url(#shadow-card)" opacity={p3_ease}>
                        <rect x="1280" y="170" width="560" height="730" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        
                        <rect x="1310" y="200" width="500" height="56" rx="10" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5" />
                        <text x="1330" y="235" font-family={FONT} font-size="20" font-weight="700" fill={COLOR_GREEN}>
                            "3. Нормалізація: P = exp(z) / sum"
                        </text>

                        <text x="1310" y="285" font-family={FONT} font-size="15" font-weight="500" fill={TEXT_MUTED}>
                            "Розподіл ймовірностей (кожна в діапазоні 0..1):"
                        </text>

                        {
                            (0..3).map(|i| {
                                let y = row_ys[i];
                                let prob = probs[i];
                                let prob_bar_w = (prob * 410.0 * p3_ease).max(12.0);
                                let is_winner = i == 0;
                                let winner_stroke = if is_winner { "#059669" } else { "none" };
                                let winner_stroke_w = if is_winner { "2.5" } else { "0" };

                                fframes::svgr!(
                                    <g filter={if is_winner && winner_pulse > 0.0 { "url(#glow-winner)" } else { "" }}>
                                        <text x="1310" y={y} font-family={FONT} font-size="18" font-weight="700" fill={TEXT_MAIN}>
                                            {class_names[i]}
                                        </text>

                                        {
                                            if is_winner {
                                                fframes::svgr!(
                                                    <g>
                                                        <rect x="1560" y={y - 18.0} width="140" height="26" rx="6" fill="#DCFCE7" stroke="#86EFAC" stroke-width="1.0" />
                                                        <text x="1630" y={y} font-family={FONT} font-size="13" font-weight="700" fill="#15803D" text-anchor="middle">
                                                            "[OK] ПЕРЕМОЖЕЦЬ"
                                                        </text>
                                                    </g>
                                                )
                                            } else {
                                                fframes::svgr!(<g></g>)
                                            }
                                        }

                                        <text x="1800" y={y} font-family={FONT} font-size="20" font-weight="700" fill={if is_winner { COLOR_GREEN } else { TEXT_MAIN }} text-anchor="end">
                                            {format!("{:.1}%", prob * 100.0 * p3_ease)}
                                        </text>

                                        <rect x="1310" y={y + 12.0} width="410" height="24" rx="6" fill="#F1F5F9" stroke="#E2E8F0" stroke-width="1.0" />
                                        <rect x="1310" y={y + 12.0} width={prob_bar_w} height="24" rx="6" fill={if is_winner { COLOR_GREEN } else { "#64748B" }} stroke={winner_stroke} stroke-width={winner_stroke_w} />
                                    </g>
                                )
                            }).collect::<Vec<_>>()
                        }

                        <rect x="1305" y="710" width="510" height="100" rx="10" fill="#ECFDF5" stroke="#6EE7B7" stroke-width="1.5" />
                        <text x="1330" y="745" font-family={FONT} font-size="16" font-weight="700" fill="#065F46">
                            "Загальна сума ймовірностей:"
                        </text>
                        <text x="1330" y="785" font-family={FONT} font-size="22" font-weight="700" fill={COLOR_GREEN}>
                            "65.90% + 24.24% + 9.86% = 100.00% (1.0)"
                        </text>
                    </g>

                    // ================= FOOTER =================
                    <circle cx="100" cy="980" r="8" fill={COLOR_BLUE} />
                    <text x="120" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Логіти (сирий скор)"
                    </text>

                    <circle cx="340" cy="980" r="8" fill={COLOR_PURPLE} />
                    <text x="360" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Експонента (нелінійне підсилення)"
                    </text>

                    <circle cx="680" cy="980" r="8" fill={COLOR_GREEN} />
                    <text x="700" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Ймовірності Softmax (впевненість мережі)"
                    </text>

                    <text x="1840" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MUTED} text-anchor="end">
                        "kostyl.dev • Інженерний практикум з нейромереж"
                    </text>

                    // Bottom progress line
                    <line x1="80" y1="1020" x2={80.0 + 1760.0 * (t / 10.0)} y2="1020" stroke={COLOR_GREEN} stroke-width="4.0" />
                </g>
            </svg>
        )
    }
}
