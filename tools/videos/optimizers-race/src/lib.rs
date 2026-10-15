//! Optimizers Race in Ravine visualization using fframes.
//!
//! Visualizes how 3 optimization algorithms behave on an anisotropic ravine (loss surface with ill-conditioned curvature):
//! 1. Vanilla SGD: bounces violently between steep walls, very slow forward progress.
//! 2. SGD + Momentum: accumulates velocity along the ravine floor, canceling transverse oscillations.
//! 3. Adam: adapts per-parameter learning rates, converging rapidly and smoothly directly into the global optimum.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct OptMedia, "media");

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

const COLOR_SGD: &str = "#DC2626";     // Red
const COLOR_MOM: &str = "#7C3AED";     // Purple
const COLOR_ADAM: &str = "#059669";    // Green

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

pub struct OptVideo<'a> {
    pub media: &'a OptMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> OptVideo<'a> {
    pub fn new(media: &'a OptMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for OptVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("OptVideo").finish()
    }
}

impl fframes::Video for OptVideo<'_> {
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

        // Progress of animation: 0.0 at t=1.0s, 1.0 at t=7.5s
        let progress = clamp((t - 1.0) / 6.5, 0.0, 1.0);

        // Precompute Trajectories (25 steps)
        // Target Minimum at (0, 0)
        // Starting Point at (-3.8, 2.2)
        const STEPS: usize = 25;

        // 1. SGD trajectory (oscillatory)
        let mut traj_sgd = [(0.0_f32, 0.0_f32); STEPS];
        let mut sx = -3.8_f32;
        let mut sy = 2.2_f32;
        traj_sgd[0] = (sx, sy);
        for i in 1..STEPS {
            sx -= 0.08 * (0.2 * sx);
            sy -= 0.44 * (4.0 * sy); // violent sign flip
            traj_sgd[i] = (sx, sy);
        }

        // 2. Momentum trajectory (smooth curved path)
        let mut traj_mom = [(0.0_f32, 0.0_f32); STEPS];
        let mut mx = -3.8_f32;
        let mut my = 2.2_f32;
        let mut mvx = 0.0_f32;
        let mut mvy = 0.0_f32;
        traj_mom[0] = (mx, my);
        for i in 1..STEPS {
            mvx = 0.82 * mvx + 0.15 * (0.35 * mx);
            mvy = 0.70 * mvy + 0.18 * (3.5 * my);
            mx -= mvx;
            my -= mvy;
            traj_mom[i] = (mx, my);
        }

        // 3. Adam trajectory (adaptive diagonal direct path)
        let mut traj_adam = [(0.0_f32, 0.0_f32); STEPS];
        let mut ax = -3.8_f32;
        let mut ay = 2.2_f32;
        let mut amx = 0.0_f32;
        let mut amy = 0.0_f32;
        let mut avx = 0.0_f32;
        let mut avy = 0.0_f32;
        traj_adam[0] = (ax, ay);
        for i in 1..STEPS {
            let gx = 0.2 * ax;
            let gy = 4.0 * ay;
            amx = 0.85 * amx + 0.15 * gx;
            amy = 0.85 * amy + 0.15 * gy;
            avx = 0.95 * avx + 0.05 * gx * gx;
            avy = 0.95 * avy + 0.05 * gy * gy;
            let step_x = 0.38 * (amx / (avx.sqrt() + 1e-4));
            let step_y = 0.38 * (amy / (avy.sqrt() + 1e-4));
            ax -= step_x;
            ay -= step_y;
            traj_adam[i] = (ax, ay);
        }

        // Current points based on progress
        let cur_step_f = progress * (STEPS - 1) as f32;
        let s_idx = (cur_step_f.floor() as usize).min(STEPS - 2);
        let s_frac = cur_step_f.fract();

        let interp = |traj: &[(f32, f32); STEPS]| -> (f32, f32) {
            let p1 = traj[s_idx];
            let p2 = traj[s_idx + 1];
            (p1.0 + (p2.0 - p1.0) * s_frac, p1.1 + (p2.1 - p1.1) * s_frac)
        };

        let pt_sgd = interp(&traj_sgd);
        let pt_mom = interp(&traj_mom);
        let pt_adam = interp(&traj_adam);

        // Coordinate transforms onto landscape
        // Minimum at cx = 1050, cy = 540
        let to_screen = |(x, y): (f32, f32)| -> (f32, f32) {
            let cx = 1050.0_f32;
            let cy = 540.0_f32;
            (cx + x * 205.0, cy - y * 140.0)
        };

        let screen_sgd = to_screen(pt_sgd);
        let screen_mom = to_screen(pt_mom);
        let screen_adam = to_screen(pt_adam);
        let screen_min = to_screen((0.0, 0.0));

        // SVG polyline generators up to current step
        let make_trail = |traj: &[(f32, f32); STEPS], cur_pt: (f32, f32)| -> String {
            let mut pts = String::new();
            for i in 0..=s_idx {
                let sp = to_screen(traj[i]);
                pts.push_str(&format!("{:.1},{:.1} ", sp.0, sp.1));
            }
            pts.push_str(&format!("{:.1},{:.1}", cur_pt.0, cur_pt.1));
            pts
        };

        let trail_sgd = make_trail(&traj_sgd, screen_sgd);
        let trail_mom = make_trail(&traj_mom, screen_mom);
        let trail_adam = make_trail(&traj_adam, screen_adam);

        // Contour ellipse levels
        let contour_levels = [0.4, 0.9, 1.6, 2.5, 3.8, 5.4, 7.5];

        // Winner pulse for Adam (t > 4.5s)
        let adam_pulse = if t > 4.5 && t < 9.0 {
            0.5 + 0.5 * ((t - 4.5) * 6.0).sin()
        } else {
            0.0
        };

        fframes::svgr!(
            <svg viewBox="0 0 1920 1080" width="1920" height="1080">
                <defs>
                    <filter id="shadow-card" x="-4%" y="-4%" width="108%" height="112%">
                        <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#0F172A" flood-opacity="0.06" />
                    </filter>
                    <filter id="shadow-ball" x="-30%" y="-30%" width="160%" height="160%">
                        <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0F172A" flood-opacity="0.25" />
                    </filter>
                    <filter id="glow-winner" x="-30%" y="-30%" width="160%" height="160%">
                        <feDropShadow dx="0" dy="0" stdDeviation="12" flood-color="#059669" flood-opacity="0.40" />
                    </filter>
                    <clipPath id="clip-landscape">
                        <rect x="80" y="160" width="1240" height="750" rx="20" />
                    </clipPath>
                    <pattern id="dot-grid" width="30" height="30" patternUnits="userSpaceOnUse">
                        <circle cx="2" cy="2" r="1.2" fill={BG_DOT} />
                    </pattern>
                </defs>

                // Background
                <rect width="1920" height="1080" fill={BG_COLOR} />
                <rect width="1920" height="1080" fill="url(#dot-grid)" opacity="0.8" />

                <g opacity={master_opacity}>
                    // ================= HEADER =================
                    <text x="80" y="75" font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN}>
                        "Гонка оптимізаторів у вузькому яру (Ravine Optimization)"
                    </text>
                    <text x="80" y="112" font-family={FONT} font-size="18" font-weight="500" fill={TEXT_MUTED}>
                        "Ландшафт втрат з високою анізотропією: круті стінки вздовж Y та пологий схил до мінімуму вздовж X"
                    </text>

                    // ================= LEFT: 2D CONTOUR LANDSCAPE =================
                    <g filter="url(#shadow-card)">
                        <rect x="80" y="160" width="1240" height="750" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                        
                        <g clip-path="url(#clip-landscape)">
                            // Landscape Gridlines
                            <line x1={screen_min.0} y1="160" x2={screen_min.0} y2="910" stroke="#F1F5F9" stroke-width="2.0" stroke-dasharray="4 4" />
                            <line x1="80" y1={screen_min.1} x2="1320" y2={screen_min.1} stroke="#F1F5F9" stroke-width="2.0" stroke-dasharray="4 4" />

                            // Concentric Elliptical Contours
                            {
                                contour_levels.iter().map(|&c| {
                                    let rx = (c / 0.08_f32).sqrt() * 105.0;
                                    let ry = (c / 1.8_f32).sqrt() * 65.0;
                                    fframes::svgr!(
                                        <g>
                                            <ellipse cx={screen_min.0} cy={screen_min.1} rx={rx} ry={ry} fill="none" stroke="#E2E8F0" stroke-width="1.8" />
                                            <text x={screen_min.0 - rx + 10.0} y={screen_min.1 - 4.0} font-family={FONT} font-size="11" font-weight="600" fill="#94A3B8">
                                                {format!("L={:.1}", c)}
                                            </text>
                                        </g>
                                    )
                                }).collect::<Vec<_>>()
                            }

                            // Start point marker
                            {
                                let sp = to_screen((-3.8, 2.2));
                                fframes::svgr!(
                                    <g>
                                        <circle cx={sp.0} cy={sp.1} r="7" fill="#64748B" />
                                        <text x={sp.0} y={sp.1 - 16.0} font-family={FONT} font-size="14" font-weight="700" fill="#475569" text-anchor="middle">
                                            "СТАРТ W0"
                                        </text>
                                    </g>
                                )
                            }

                            // Target Minimum Marker (Global Optimum)
                            <circle cx={screen_min.0} cy={screen_min.1} r="18" fill="#ECFDF5" stroke={COLOR_ADAM} stroke-width="2.5" />
                            <circle cx={screen_min.0} cy={screen_min.1} r="6" fill={COLOR_ADAM} />
                            <text x={screen_min.0} y={screen_min.1 + 38.0} font-family={FONT} font-size="15" font-weight="700" fill={COLOR_ADAM} text-anchor="middle">
                                "Мінімум W*"
                            </text>

                            // Trajectory Trails
                            // 1. SGD Trail (Red)
                            <polyline points={trail_sgd} fill="none" stroke={COLOR_SGD} stroke-width="2.5" stroke-linecap="round" opacity="0.8" />
                            // 2. Momentum Trail (Purple)
                            <polyline points={trail_mom} fill="none" stroke={COLOR_MOM} stroke-width="3.2" stroke-linecap="round" stroke-dasharray="6 4" opacity="0.9" />
                            // 3. Adam Trail (Green)
                            <polyline points={trail_adam} fill="none" stroke={COLOR_ADAM} stroke-width="4.0" stroke-linecap="round" opacity="0.95" />

                            // Balls
                            // SGD Ball
                            <circle cx={screen_sgd.0} cy={screen_sgd.1} r="13" fill={COLOR_SGD} stroke="#FFFFFF" stroke-width="2.5" filter="url(#shadow-ball)" />
                            // Momentum Ball
                            <circle cx={screen_mom.0} cy={screen_mom.1} r="14" fill={COLOR_MOM} stroke="#FFFFFF" stroke-width="2.5" filter="url(#shadow-ball)" />
                            // Adam Ball
                            <circle cx={screen_adam.0} cy={screen_adam.1} r="16" fill={COLOR_ADAM} stroke="#FFFFFF" stroke-width="3.0" filter={if adam_pulse > 0.0 { "url(#glow-winner)" } else { "url(#shadow-ball)" }} />
                        </g>

                        // Overlay Title inside landscape
                        <rect x="105" y="185" width="310" height="42" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.0" opacity="0.95" />
                        <text x="120" y="212" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN}>
                            "Топографічний профіль яру L(x, y)"
                        </text>
                    </g>

                    // ================= RIGHT: COMPARATIVE CARDS =================
                    <g>
                        // Card 1: SGD
                        <g filter="url(#shadow-card)">
                            <rect x="1350" y="160" width="490" height="230" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                            <rect x="1375" y="185" width="180" height="34" rx="8" fill="#FEF2F2" stroke="#FECACA" stroke-width="1.0" />
                            <text x="1465" y="208" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_SGD} text-anchor="middle">
                                "1. Vanilla SGD"
                            </text>
                            
                            <text x="1375" y="248" font-family={FONT} font-size="14" font-weight="600" fill={TEXT_MUTED}>
                                "Механіка: чистий градієнт без пам'яті"
                            </text>
                            <text x="1375" y="282" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_SGD}>
                                "[!] Б'ється об стінки яру (zig-zag)"
                            </text>
                            <text x="1375" y="312" font-family={FONT} font-size="14" font-weight="500" fill={TEXT_MUTED}>
                                "Горизонтальний поступ повільний через коливання."
                            </text>
                            <rect x="1375" y="340" width="440" height="32" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.0" />
                            <text x="1395" y="362" font-family={FONT} font-size="13" font-weight="700" fill="#64748B">
                                {format!("Поточні координати: ({:.2}, {:.2})", pt_sgd.0, pt_sgd.1)}
                            </text>
                        </g>

                        // Card 2: Momentum
                        <g filter="url(#shadow-card)">
                            <rect x="1350" y="420" width="490" height="230" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                            <rect x="1375" y="445" width="220" height="34" rx="8" fill="#FAF5FF" stroke="#E9D5FF" stroke-width="1.0" />
                            <text x="1485" y="468" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_MOM} text-anchor="middle">
                                "2. SGD + Momentum"
                            </text>
                            
                            <text x="1375" y="508" font-family={FONT} font-size="14" font-weight="600" fill={TEXT_MUTED}>
                                "Механіка: v_t = beta*v_(t-1) + (1-beta)*grad"
                            </text>
                            <text x="1375" y="542" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_MOM}>
                                "[~] Інерція гасить поперечні коливання"
                            </text>
                            <text x="1375" y="572" font-family={FONT} font-size="14" font-weight="500" fill={TEXT_MUTED}>
                                "Імпульси Y компенсуються, швидкість X зростає вздовж дна."
                            </text>
                            <rect x="1375" y="600" width="440" height="32" rx="6" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.0" />
                            <text x="1395" y="622" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_MOM}>
                                {format!("Поточні координати: ({:.2}, {:.2})", pt_mom.0, pt_mom.1)}
                            </text>
                        </g>

                        // Card 3: Adam
                        <g filter="url(#shadow-card)">
                            <rect x="1350" y="680" width="490" height="230" rx="16" fill={CARD_BG} stroke="#86EFAC" stroke-width="2.0" />
                            <rect x="1375" y="705" width="310" height="34" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1.0" />
                            <text x="1530" y="728" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_ADAM} text-anchor="middle">
                                "3. Adam (Adaptive Moment)"
                            </text>
                            
                            <text x="1375" y="768" font-family={FONT} font-size="14" font-weight="600" fill={TEXT_MUTED}>
                                "Механіка: Momentum + адаптивний крок sqrt(v)"
                            </text>
                            <text x="1375" y="802" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_ADAM}>
                                "[OK] ПЕРЕМОЖЕЦЬ: Прямий спуск до W*"
                            </text>
                            <text x="1375" y="832" font-family={FONT} font-size="14" font-weight="500" fill={TEXT_MUTED}>
                                "Зменшує крок по крутій осі Y та прискорює по осі X."
                            </text>
                            <rect x="1375" y="860" width="440" height="32" rx="6" fill="#ECFDF5" stroke="#6EE7B7" stroke-width="1.0" />
                            <text x="1395" y="882" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_ADAM}>
                                {format!("Поточні координати: ({:.2}, {:.2})", pt_adam.0, pt_adam.1)}
                            </text>
                        </g>
                    </g>

                    // ================= FOOTER =================
                    <circle cx="100" cy="980" r="8" fill={COLOR_SGD} />
                    <text x="120" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Vanilla SGD (осциляції)"
                    </text>

                    <circle cx="360" cy="980" r="8" fill={COLOR_MOM} />
                    <text x="380" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "SGD + Momentum (інерція)"
                    </text>

                    <circle cx="680" cy="980" r="8" fill={COLOR_ADAM} />
                    <text x="700" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MAIN}>
                        "Adam (адаптивний швидкісний спуск)"
                    </text>

                    <text x="1840" y="986" font-family={FONT} font-size="16" font-weight="600" fill={TEXT_MUTED} text-anchor="end">
                        "kostyl.dev • Інженерний практикум з нейромереж"
                    </text>

                    // Bottom progress line
                    <line x1="80" y1="1020" x2={80.0 + 1760.0 * (t / 10.0)} y2="1020" stroke={COLOR_ADAM} stroke-width="4.0" />
                </g>
            </svg>
        )
    }
}
