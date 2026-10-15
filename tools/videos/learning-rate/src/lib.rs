//! Learning Rate Behavior visualization using fframes.
//!
//! Visualizes how the learning rate alpha influences optimization on a convex loss bowl:
//! 1. Too Small (lr = 0.05): painfully slow progress, requires too many epochs.
//! 2. Optimal (lr = 0.35): rapid, smooth convergence directly into the global minimum.
//! 3. Too Large (lr = 1.08): overshooting oscillations and explosive divergence (NaN).

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct LRMedia, "media");

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
const COLOR_GREEN: &str = "#059669";
const COLOR_RED: &str = "#DC2626";
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

pub struct LRVideo<'a> {
    pub media: &'a LRMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> LRVideo<'a> {
    pub fn new(media: &'a LRMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for LRVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("LRVideo").finish()
    }
}

impl fframes::Video for LRVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(255, 255, 255);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.0)..AudioTimestamp::Eof).gain_db(-2.0),
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

        // Step progression: 6 discrete steps between t = 1.2s and t = 7.2s
        let step_time = 1.0_f32;
        let anim_t = (t - 1.2).max(0.0);
        let current_step_f = (anim_t / step_time).min(5.99);
        let step_idx = current_step_f.floor() as usize;
        let step_fraction = current_step_f.fract();
        let ease_step = ease_in_out(step_fraction);

        // Precomputed trajectories for 6 steps:
        // Case 1: Small lr (factor 0.90)
        let mut traj_small = [-2.20_f32; 7];
        for i in 1..7 {
            traj_small[i] = traj_small[i - 1] * 0.88;
        }

        // Case 2: Optimal lr (factor 0.30)
        let mut traj_opt = [-2.20_f32; 7];
        for i in 1..7 {
            traj_opt[i] = traj_opt[i - 1] * 0.32;
        }

        // Case 3: Too large lr (factor -1.16)
        let mut traj_large = [-1.15_f32; 7];
        for i in 1..7 {
            traj_large[i] = traj_large[i - 1] * -1.18;
        }

        // Current interpolated positions
        let cur_w_small = traj_small[step_idx] + (traj_small[step_idx + 1] - traj_small[step_idx]) * ease_step;
        let cur_w_opt = traj_opt[step_idx] + (traj_opt[step_idx + 1] - traj_opt[step_idx]) * ease_step;
        let cur_w_large = traj_large[step_idx] + (traj_large[step_idx + 1] - traj_large[step_idx]) * ease_step;

        // Card Layout
        let card_w = 560.0_f32;
        let card_h = 740.0_f32;
        let card_y = 170.0_f32;
        let xs = [80.0_f32, 680.0_f32, 1280.0_f32];

        // Parabola conversion within card:
        // center x = card_x + card_w / 2 = card_x + 280
        // vertex y = 620
        // curve: y(w) = 620 - 45 * w^2
        let to_canvas = |card_left: f32, w: f32| -> (f32, f32) {
            let cx = card_left + 280.0;
            let cy = 620.0;
            let px = cx + w * 95.0;
            let py = cy - (w * w) * 38.0;
            (px, py)
        };

        // Generate parabola SVG path for a card
        let make_parabola_path = |card_left: f32| -> String {
            let mut d = String::new();
            for i in 0..=50 {
                let w = -2.5 + (5.0 / 50.0) * (i as f32);
                let (px, py) = to_canvas(card_left, w);
                if i == 0 {
                    d.push_str(&format!("M {:.1},{:.1}", px, py));
                } else {
                    d.push_str(&format!(" L {:.1},{:.1}", px, py));
                }
            }
            d
        };

        let path_c1 = make_parabola_path(xs[0]);
        let path_c2 = make_parabola_path(xs[1]);
        let path_c3 = make_parabola_path(xs[2]);

        let (ball1_x, ball1_y) = to_canvas(xs[0], cur_w_small);
        let (ball2_x, ball2_y) = to_canvas(xs[1], cur_w_opt);
        let (ball3_x, ball3_y) = to_canvas(xs[2], cur_w_large);

        let loss1 = cur_w_small * cur_w_small;
        let loss2 = cur_w_opt * cur_w_opt;
        let loss3 = cur_w_large * cur_w_large;

        fframes::svgr!(
            <svg viewBox="0 0 1920 1080" width="1920" height="1080">
                <defs>
                    <filter id="shadow-card" x="-4%" y="-4%" width="108%" height="112%">
                        <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.06" />
                    </filter>
                    <filter id="shadow-ball" x="-30%" y="-30%" width="160%" height="160%">
                        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.25" />
                    </filter>
                    <clipPath id="clip-card1">
                        <rect x={xs[0]} y={card_y} width={card_w} height={card_h} rx="18" />
                    </clipPath>
                    <clipPath id="clip-card2">
                        <rect x={xs[1]} y={card_y} width={card_w} height={card_h} rx="18" />
                    </clipPath>
                    <clipPath id="clip-card3">
                        <rect x={xs[2]} y={card_y} width={card_w} height={card_h} rx="18" />
                    </clipPath>
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
                        "Швидкість навчання (Learning Rate alpha): вплив на збіжність"
                    </text>
                    <text x="80" y="112" font-family={FONT} font-size="18" font-weight="500" fill={TEXT_MUTED}>
                        "Оновлення параметрів w = w - alpha * grad • Головний гіперпараметр градієнтного спуску"
                    </text>

                    // ================= CARD 1: TOO SMALL =================
                    <g filter="url(#shadow-card)">
                        <rect x={xs[0]} y={card_y} width={card_w} height={card_h} rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        
                        <rect x={xs[0] + 30.0} y={card_y + 25.0} width={card_w - 60.0} height="52" rx="10" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1.5" />
                        <text x={xs[0] + 50.0} y={card_y + 58.0} font-family={FONT} font-size="19" font-weight="700" fill={COLOR_AMBER}>
                            "1. Занадто малий (lr = 0.05)"
                        </text>

                        <text x={xs[0] + 30.0} y={card_y + 110.0} font-family={FONT} font-size="15" font-weight="500" fill={TEXT_MUTED}>
                            "Мікроскопічні кроки: застрягає на схилі"
                        </text>

                        // Parabola & Curve Content (Clipped)
                        <g clip-path="url(#clip-card1)">
                            // Horizontal minimum baseline
                            <line x1={xs[0] + 40.0} y1="620" x2={xs[0] + card_w - 40.0} y2="620" stroke="#E2E8F0" stroke-width="2.0" stroke-dasharray="4 4" />
                            // Parabola curve
                            <path d={path_c1} fill="none" stroke="#94A3B8" stroke-width="3.5" />

                            // Historic dots for small steps
                            {
                                (0..=step_idx).map(|s| {
                                    let (px, py) = to_canvas(xs[0], traj_small[s]);
                                    fframes::svgr!(
                                        <circle cx={px} cy={py} r="4.5" fill={COLOR_AMBER} opacity="0.6" />
                                    )
                                }).collect::<Vec<_>>()
                            }

                            // Active Ball
                            <circle cx={ball1_x} cy={ball1_y} r="14" fill={COLOR_AMBER} stroke="#FFFFFF" stroke-width="2.5" filter="url(#shadow-ball)" />
                        </g>

                        // Bottom Metrics Card
                        <rect x={xs[0] + 25.0} y={card_y + 510.0} width={card_w - 50.0} height="175" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5" />
                        <text x={xs[0] + 45.0} y={card_y + 545.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED}>
                            {format!("Крок спуску: {} / 6", step_idx + 1)}
                        </text>
                        <text x={xs[0] + 45.0} y={card_y + 580.0} font-family={FONT} font-size="20" font-weight="700" fill={COLOR_AMBER}>
                            {format!("Loss L(w) = {:.3}", loss1)}
                        </text>

                        <rect x={xs[0] + 45.0} y={card_y + 605.0} width={card_w - 90.0} height="60" rx="8" fill="#FFFBEB" stroke="#FCD34D" stroke-width="1.0" />
                        <text x={xs[0] + 60.0} y={card_y + 632.0} font-family={FONT} font-size="14" font-weight="700" fill="#B45309">
                            "[!] Наслідок: надповільне навчання"
                        </text>
                        <text x={xs[0] + 60.0} y={card_y + 653.0} font-family={FONT} font-size="13" font-weight="500" fill="#92400E">
                            "Потрібні тисячі епох, ризик застрягти."
                        </text>
                    </g>

                    // ================= CARD 2: OPTIMAL =================
                    <g filter="url(#shadow-card)">
                        <rect x={xs[1]} y={card_y} width={card_w} height={card_h} rx="18" fill={CARD_BG} stroke="#86EFAC" stroke-width="2.0" />
                        
                        <rect x={xs[1] + 30.0} y={card_y + 25.0} width={card_w - 60.0} height="52" rx="10" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.5" />
                        <text x={xs[1] + 50.0} y={card_y + 58.0} font-family={FONT} font-size="19" font-weight="700" fill={COLOR_GREEN}>
                            "2. Оптимальний (lr = 0.35)"
                        </text>

                        <text x={xs[1] + 30.0} y={card_y + 110.0} font-family={FONT} font-size="15" font-weight="500" fill={TEXT_MUTED}>
                            "Швидка та впевнена збіжність на дно чаші"
                        </text>

                        // Parabola & Curve Content (Clipped)
                        <g clip-path="url(#clip-card2)">
                            <line x1={xs[1] + 40.0} y1="620" x2={xs[1] + card_w - 40.0} y2="620" stroke="#E2E8F0" stroke-width="2.0" stroke-dasharray="4 4" />
                            <path d={path_c2} fill="none" stroke="#94A3B8" stroke-width="3.5" />

                            // Historic dots & trajectory lines
                            {
                                (0..=step_idx).map(|s| {
                                    let (px, py) = to_canvas(xs[1], traj_opt[s]);
                                    fframes::svgr!(
                                        <circle cx={px} cy={py} r="5.0" fill={COLOR_GREEN} opacity="0.7" />
                                    )
                                }).collect::<Vec<_>>()
                            }

                            // Target Minimum Flag at bottom
                            <line x1={xs[1] + 280.0} y1="590" x2={xs[1] + 280.0} y2="620" stroke={COLOR_GREEN} stroke-width="2.5" />
                            <circle cx={xs[1] + 280.0} cy="620" r="4.0" fill={COLOR_GREEN} />

                            // Active Ball
                            <circle cx={ball2_x} cy={ball2_y} r="16" fill={COLOR_GREEN} stroke="#FFFFFF" stroke-width="2.5" filter="url(#shadow-ball)" />
                        </g>

                        // Bottom Metrics Card
                        <rect x={xs[1] + 25.0} y={card_y + 510.0} width={card_w - 50.0} height="175" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5" />
                        <text x={xs[1] + 45.0} y={card_y + 545.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED}>
                            {format!("Крок спуску: {} / 6", step_idx + 1)}
                        </text>
                        <text x={xs[1] + 45.0} y={card_y + 580.0} font-family={FONT} font-size="20" font-weight="700" fill={COLOR_GREEN}>
                            {format!("Loss L(w) = {:.3}", loss2)}
                        </text>

                        <rect x={xs[1] + 45.0} y={card_y + 605.0} width={card_w - 90.0} height="60" rx="8" fill="#ECFDF5" stroke="#6EE7B7" stroke-width="1.0" />
                        <text x={xs[1] + 60.0} y={card_y + 632.0} font-family={FONT} font-size="14" font-weight="700" fill="#047857">
                            "[OK] Золотий стандарт: швидкий спуск"
                        </text>
                        <text x={xs[1] + 60.0} y={card_y + 653.0} font-family={FONT} font-size="13" font-weight="500" fill="#065F46">
                            "Мінімум досягається за лічені ітерації."
                        </text>
                    </g>

                    // ================= CARD 3: TOO LARGE =================
                    <g filter="url(#shadow-card)">
                        <rect x={xs[2]} y={card_y} width={card_w} height={card_h} rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        
                        <rect x={xs[2] + 30.0} y={card_y + 25.0} width={card_w - 60.0} height="52" rx="10" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.5" />
                        <text x={xs[2] + 50.0} y={card_y + 58.0} font-family={FONT} font-size="19" font-weight="700" fill={COLOR_RED}>
                            "3. Занадто великий (lr = 1.08)"
                        </text>

                        <text x={xs[2] + 30.0} y={card_y + 110.0} font-family={FONT} font-size="15" font-weight="500" fill={TEXT_MUTED}>
                            "Перестрибування та виліт у нескінченність"
                        </text>

                        // Parabola & Curve Content (Clipped)
                        <g clip-path="url(#clip-card3)">
                            <line x1={xs[2] + 40.0} y1="620" x2={xs[2] + card_w - 40.0} y2="620" stroke="#E2E8F0" stroke-width="2.0" stroke-dasharray="4 4" />
                            <path d={path_c3} fill="none" stroke="#94A3B8" stroke-width="3.5" />

                            // Historic overshoot lines
                            {
                                (0..step_idx).map(|s| {
                                    let (p1x, p1y) = to_canvas(xs[2], traj_large[s]);
                                    let (p2x, p2y) = to_canvas(xs[2], traj_large[s + 1]);
                                    fframes::svgr!(
                                        <g>
                                            <line x1={p1x} y1={p1y} x2={p2x} y2={p2y} stroke={COLOR_RED} stroke-width="2.0" stroke-dasharray="4 4" opacity="0.6" />
                                            <circle cx={p1x} cy={p1y} r="4.5" fill={COLOR_RED} opacity="0.6" />
                                        </g>
                                    )
                                }).collect::<Vec<_>>()
                            }

                            // Active Ball
                            <circle cx={ball3_x} cy={ball3_y} r="14" fill={COLOR_RED} stroke="#FFFFFF" stroke-width="2.5" filter="url(#shadow-ball)" />
                        </g>

                        // Bottom Metrics Card
                        <rect x={xs[2] + 25.0} y={card_y + 510.0} width={card_w - 50.0} height="175" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5" />
                        <text x={xs[2] + 45.0} y={card_y + 545.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED}>
                            {format!("Крок спуску: {} / 6", step_idx + 1)}
                        </text>
                        <text x={xs[2] + 45.0} y={card_y + 580.0} font-family={FONT} font-size="20" font-weight="700" fill={COLOR_RED}>
                            {if step_idx >= 4 {
                                "Loss L(w) -> EXPLODING (NaN)".to_string()
                            } else {
                                format!("Loss L(w) = {:.3}", loss3)
                            }}
                        </text>

                        <rect x={xs[2] + 45.0} y={card_y + 605.0} width={card_w - 90.0} height="60" rx="8" fill="#FEF2F2" stroke="#FCA5A5" stroke-width="1.0" />
                        <text x={xs[2] + 60.0} y={card_y + 632.0} font-family={FONT} font-size="14" font-weight="700" fill="#B91C1C">
                            "[X] Катастрофа: розбіжність (Divergence)"
                        </text>
                        <text x={xs[2] + 60.0} y={card_y + 653.0} font-family={FONT} font-size="13" font-weight="500" fill="#991B1B">
                            "Мережа ламається, ваги отримують NaN/Inf."
                        </text>
                    </g>

                    // ================= FOOTER =================
                    <circle cx="100" cy="980" r="8" fill={COLOR_AMBER} />
                    <text x="120" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Малий крок (повільна збіжність)"
                    </text>

                    <circle cx="440" cy="980" r="8" fill={COLOR_GREEN} />
                    <text x="460" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Оптимальний крок (швидкий мінімум)"
                    </text>

                    <circle cx="780" cy="980" r="8" fill={COLOR_RED} />
                    <text x="800" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Великий крок (виліт та вибух градієнтів)"
                    </text>

                    <text x="1840" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MUTED} text-anchor="end">
                        "kostyl.dev • Інженерний практикум з нейромереж"
                    </text>

                    // Bottom progress line
                    <line x1="80" y1="1020" x2={80.0 + 1760.0 * (t / 10.0)} y2="1020" stroke={COLOR_BLUE} stroke-width="4.0" />
                </g>
            </svg>
        )
    }
}
