//! Vanishing Gradient visualization using fframes.
//!
//! Renders an animated comparison of backward gradient flow through 5 layers:
//! Top:    Sigmoid (derivative <= 0.25) -> Gradient rapidly vanishes to 0.001.
//! Bottom: ReLU (derivative = 1.0 for z>0) -> Gradient flows without attenuation.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct VanishingMedia, "media");

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

const COLOR_BLUE: &str = "#2563EB";
const COLOR_RED: &str = "#DC2626";
const COLOR_RED_LIGHT: &str = "#FEF2F2";
const COLOR_GREEN: &str = "#059669";
const COLOR_GREEN_LIGHT: &str = "#ECFDF5";
const COLOR_AMBER: &str = "#D97706";
const COLOR_PURPLE: &str = "#7C3AED";
const COLOR_PURPLE_LIGHT: &str = "#F3E8FF";

const LINE_COLOR: &str = "#CBD5E1";

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

pub struct VanishingVideo<'a> {
    pub media: &'a VanishingMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> VanishingVideo<'a> {
    pub fn new(media: &'a VanishingMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for VanishingVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("VanishingVideo").finish()
    }
}

impl fframes::Video for VanishingVideo<'_> {
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
            AudioTrack::new("activate.wav", AudioTimestamp::Second(5.5)..AudioTimestamp::Eof).gain_db(0.0),
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

        // Backward wave animation (flows from Right Layer 5 to Left Layer 1)
        // Travels between t = 1.5s and t = 5.5s, then repeats
        let wave_raw = clamp((t - 1.2) / 4.2, 0.0, 1.0);
        let wave_p = ease_in_out(wave_raw) * loop_reset;

        // 5 Layers X-positions (Left = Layer 1 / Input, Right = Layer 5 / Output)
        let layer_xs = [320.0_f32, 630.0, 940.0, 1250.0, 1560.0];
        let layer_names = ["Шар 1 (Вхід)", "Шар 2", "Шар 3", "Шар 4", "Шар 5 (Вихід)"];

        // Gradient values:
        // Sigmoid: 1.0 -> 0.25 -> 0.062 -> 0.016 -> 0.001
        let sig_grads = [0.001_f32, 0.016, 0.062, 0.250, 1.000];
        // ReLU: 1.0 -> 1.0 -> 1.0 -> 1.0 -> 1.0
        let relu_grads = [1.000_f32, 1.000, 1.000, 1.000, 1.000];

        // Top Row Y (Sigmoid)
        let top_row_y = 330.0_f32;
        // Bottom Row Y (ReLU)
        let bot_row_y = 730.0_f32;

        // Wave travels from x = layer_xs[4] (1560) down to layer_xs[0] (320)
        let current_wave_x = 1560.0 - wave_p * (1560.0 - 320.0);

        let bar_width = 1760.0_f32;
        let progress_w = (t / 10.0) * bar_width;

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <pattern id="dot-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="1.3" fill={BG_DOT} />
                    </pattern>

                    <filter id="shadow-card" x="-5%" y="-5%" width="110%" height="110%">
                        <feDropShadow dx="0" dy="4" stdDeviation="10" flood-color="#0F172A" flood-opacity="0.05" />
                    </filter>
                    <filter id="shadow-node" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.08" />
                    </filter>
                </defs>

                // Background
                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />

                // TOP HEADER
                <g opacity={intro_alpha}>
                    <rect x="80" y="28" width="1760" height="96" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" filter="url(#shadow-card)" />
                    <text x="110" y="68" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN}>
                        "Проблема згасання градієнта: Сигмоїда проти ReLU"
                    </text>
                    <text x="110" y="100" font-family={FONT} font-size="17" fill={TEXT_MUTED}>
                        "Похідна сигмоїди σ'(z) ≤ 0.25 множиться крізь шари й згасає до 0 • Похідна ReLU = 1.0 зберігає повний сигнал"
                    </text>

                    // Top Badge
                    <rect x="1440" y="50" width="370" height="50" rx="25" fill={COLOR_GREEN_LIGHT} stroke={COLOR_GREEN} stroke-width="1.5" />
                    <text x="1625" y="81" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                        "Чому Deep Learning обрав ReLU"
                    </text>
                </g>

                // ================= TOP CARD: SIGMOID (VANISHING) =================
                <g opacity={intro_alpha}>
                    <rect x="80" y="144" width="1760" height="376" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="2.0" filter="url(#shadow-card)" />

                    // Header Badge
                    <rect x="110" y="168" width="560" height="46" rx="12" fill={COLOR_PURPLE_LIGHT} stroke="#D8B4FE" stroke-width="1.5" />
                    <text x="130" y="198" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_PURPLE}>
                        "СИГМОЇДА: σ'(z) ≤ 0.25 (Градієнт катастрофічно згасає)"
                    </text>

                    // Status Callout Badge on Top Right
                    <rect x="1120" y="168" width="690" height="46" rx="12" fill={COLOR_RED_LIGHT} stroke="#FECACA" stroke-width="1.5" />
                    <text x="1465" y="197" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_RED} text-anchor="middle">
                        "[X] ПОМИЛКА: Перші шари не отримують градієнта і майже не навчаються!"
                    </text>

                    // Passive Connecting Lines
                    {
                        (0..4).map(|i| {
                            let x1 = layer_xs[i];
                            let x2 = layer_xs[i + 1];
                            fframes::svgr!(
                                <line x1={x1} y1={top_row_y} x2={x2} y2={top_row_y} stroke={LINE_COLOR} stroke-width="3.0" stroke-dasharray="8,6" />
                            )
                        }).collect::<Vec<_>>()
                    }

                    // Backward Flow Arrows (Right to Left)
                    {
                        (0..4).map(|i| {
                            let mid_x = (layer_xs[i] + layer_xs[i + 1]) / 2.0;
                            fframes::svgr!(
                                <g>
                                    <line x1={mid_x + 30.0} y1={top_row_y - 25.0} x2={mid_x - 30.0} y2={top_row_y - 25.0} stroke="#A855F7" stroke-width="2.5" />
                                    <polygon points={format!("{:.1},{:.1} {:.1},{:.1} {:.1},{:.1}", mid_x - 32.0, top_row_y - 25.0, mid_x - 22.0, top_row_y - 30.0, mid_x - 22.0, top_row_y - 20.0)} fill="#A855F7" />
                                    <text x={mid_x} y={top_row_y - 35.0} font-family={FONT} font-size="13" font-weight="700" fill="#9333EA" text-anchor="middle">
                                        "× 0.25"
                                    </text>
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }

                    // Nodes along Sigmoid Row
                    {
                        layer_xs.iter().enumerate().map(|(idx, &x)| {
                            let grad = sig_grads[idx];
                            // Node radius and opacity shrink as gradient vanishes
                            let node_r = 16.0 + 26.0 * grad.powf(0.4);
                            let node_opacity = 0.20 + 0.80 * grad.powf(0.5);
                            let is_reached = current_wave_x <= x;
                            let active_glow = if is_reached { 1.0 } else { 0.4 };

                            fframes::svgr!(
                                <g filter="url(#shadow-node)">
                                    <circle cx={x} cy={top_row_y} r={node_r + 8.0} fill="#E9D5FF" opacity={active_glow * 0.4} />
                                    <circle cx={x} cy={top_row_y} r={node_r} fill={COLOR_PURPLE} opacity={node_opacity * active_glow} stroke="#0F172A" stroke-width="2.5" />
                                    <text x={x} y={top_row_y + 60.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                                        {layer_names[idx]}
                                    </text>
                                    <rect x={x - 65.0} y={top_row_y + 75.0} width="130" height="28" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.0" />
                                    <text x={x} y={top_row_y + 94.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_PURPLE} text-anchor="middle">
                                        {format!("grad = {:.3}", grad)}
                                    </text>
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }
                </g>

                // ================= BOTTOM CARD: RELU (CONSTANT FLOW) =================
                <g opacity={intro_alpha}>
                    <rect x="80" y="540" width="1760" height="376" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="2.0" filter="url(#shadow-card)" />

                    // Header Badge
                    <rect x="110" y="564" width="560" height="46" rx="12" fill={COLOR_GREEN_LIGHT} stroke="#A7F3D0" stroke-width="1.5" />
                    <text x="130" y="594" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_GREEN}>
                        "ReLU: ReLU'(z) = 1.0 (Градієнт проходить без втрат)"
                    </text>

                    // Status Callout Badge on Top Right
                    <rect x="1120" y="564" width="690" height="46" rx="12" fill={COLOR_GREEN_LIGHT} stroke="#86EFAC" stroke-width="1.5" />
                    <text x="1465" y="593" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                        "[OK] УСПІХ: Повний градієнт 100% доходить до найперших шарів мережі!"
                    </text>

                    // Passive Connecting Lines
                    {
                        (0..4).map(|i| {
                            let x1 = layer_xs[i];
                            let x2 = layer_xs[i + 1];
                            fframes::svgr!(
                                <line x1={x1} y1={bot_row_y} x2={x2} y2={bot_row_y} stroke={LINE_COLOR} stroke-width="3.0" stroke-dasharray="8,6" />
                            )
                        }).collect::<Vec<_>>()
                    }

                    // Backward Flow Arrows (Right to Left)
                    {
                        (0..4).map(|i| {
                            let mid_x = (layer_xs[i] + layer_xs[i + 1]) / 2.0;
                            fframes::svgr!(
                                <g>
                                    <line x1={mid_x + 30.0} y1={bot_row_y - 25.0} x2={mid_x - 30.0} y2={bot_row_y - 25.0} stroke={COLOR_GREEN} stroke-width="3.0" />
                                    <polygon points={format!("{:.1},{:.1} {:.1},{:.1} {:.1},{:.1}", mid_x - 32.0, bot_row_y - 25.0, mid_x - 22.0, bot_row_y - 30.0, mid_x - 22.0, bot_row_y - 20.0)} fill={COLOR_GREEN} />
                                    <text x={mid_x} y={bot_row_y - 35.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                                        "× 1.0"
                                    </text>
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }

                    // Nodes along ReLU Row
                    {
                        layer_xs.iter().enumerate().map(|(idx, &x)| {
                            let grad = relu_grads[idx];
                            let node_r = 40.0_f32; // Full healthy radius
                            let is_reached = current_wave_x <= x;
                            let active_glow = if is_reached { 1.0 } else { 0.4 };

                            fframes::svgr!(
                                <g filter="url(#shadow-node)">
                                    <circle cx={x} cy={bot_row_y} r={node_r + 8.0} fill="#D1FAE5" opacity={active_glow * 0.5} />
                                    <circle cx={x} cy={bot_row_y} r={node_r} fill={COLOR_GREEN} stroke="#0F172A" stroke-width="2.5" />
                                    <text x={x} y={bot_row_y + 60.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                                        {layer_names[idx]}
                                    </text>
                                    <rect x={x - 75.0} y={bot_row_y + 75.0} width="150" height="28" rx="6" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.0" />
                                    <text x={x} y={bot_row_y + 94.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                                        {format!("grad = {:.3} (100%)", grad)}
                                    </text>
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }
                </g>

                // ================= FOOTER =================
                <g opacity={intro_alpha}>
                    <circle cx="120" cy="970" r="8.5" fill={COLOR_PURPLE} stroke="#0F172A" stroke-width="2.0" />
                    <text x="140" y="976" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                        "Сигмоїда: затухання градієнта у 1000 разів на 5 шарах"
                    </text>

                    <circle cx="620" cy="970" r="8.5" fill={COLOR_GREEN} stroke="#0F172A" stroke-width="2.0" />
                    <text x="640" y="976" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                        "ReLU: постійна швидкість навчання для всіх шарів"
                    </text>

                    <text x="1840" y="976" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED} text-anchor="end">
                        "kostyl.dev • Інженерний практикум з нейромереж"
                    </text>

                    // Progress Bar
                    <rect x="80" y="1000" width={bar_width} height="6" rx="3" fill="#E2E8F0" />
                    <rect x="80" y="1000" width={progress_w} height="6" rx="3" fill={COLOR_GREEN} />
                </g>
            </svg>
        )
    }
}
