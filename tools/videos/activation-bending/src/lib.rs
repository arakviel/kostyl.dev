//! Space Bending & Activation Functions visualization using fframes.
//!
//! Renders a 1920x1080 animated comparison:
//! Left:  Linear layers without activation (W2 * W1 * x + b) -> Space stays flat, classes remain inseparable.
//! Right: With non-linear activation (e.g. ReLU/Sigmoid) -> Space bends, classes become linearly separable!

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct BendingMedia, "media");

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
const COLOR_BLUE_LIGHT: &str = "#EFF6FF";
const COLOR_RED: &str = "#DC2626";
#[allow(dead_code)]
const COLOR_RED_LIGHT: &str = "#FEF2F2";
const COLOR_GREEN: &str = "#059669";
const COLOR_GREEN_LIGHT: &str = "#ECFDF5";
const COLOR_AMBER: &str = "#D97706";
const COLOR_AMBER_LIGHT: &str = "#FEF3C7";

const GRID_LINE_COLOR: &str = "#CBD5E1";
const GRID_AXIS_COLOR: &str = "#94A3B8";

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

pub struct BendingVideo<'a> {
    pub media: &'a BendingMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> BendingVideo<'a> {
    pub fn new(media: &'a BendingMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for BendingVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("BendingVideo").finish()
    }
}

impl fframes::Video for BendingVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(255, 255, 255);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.4)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(4.8)..AudioTimestamp::Eof)
                .gain_db(0.0),
        ])
    }

    fn render_frame<'a>(&'a self, frame: Frame, _ctx: &FFramesContext<'a, '_>) -> Svgr<'a> {
        let t = frame.seconds();

        // Intro fade in (0.0s -> 0.8s)
        let intro_alpha = ease_out_cubic(clamp(t / 0.8, 0.0, 1.0));

        // Seamless loop reset (9.2s -> 10.0s)
        let loop_reset = if t >= 9.2 {
            1.0 - ease_in_out(clamp((t - 9.2) / 0.8, 0.0, 1.0))
        } else {
            1.0
        };

        // Transformation progress (1.2s .. 4.2s)
        let transform_raw = clamp((t - 1.2) / 3.0, 0.0, 1.0);
        let transform_p = ease_in_out(transform_raw) * loop_reset;

        // Boundary appearance (4.5s .. 5.5s)
        let boundary_raw = clamp((t - 4.5) / 0.8, 0.0, 1.0);
        let boundary_appear = ease_in_out(boundary_raw) * loop_reset;

        // Center coordinates of inner canvases
        let left_cx = 500.0_f32;
        let left_cy = 530.0_f32;
        let right_cx = 1420.0_f32;
        let right_cy = 530.0_f32;
        let scale = 160.0_f32;

        // Points in original space:
        // 6 Blue points (inner circle r = 0.45)
        let mut blue_pts: Vec<(f32, f32)> = Vec::new();
        for i in 0..6 {
            let angle = (i as f32) * std::f32::consts::PI * 2.0 / 6.0;
            blue_pts.push((0.45 * angle.cos(), 0.45 * angle.sin()));
        }

        // 10 Red points (outer ring r = 1.05)
        let mut red_pts: Vec<(f32, f32)> = Vec::new();
        for i in 0..10 {
            let angle = (i as f32) * std::f32::consts::PI * 2.0 / 10.0 + 0.3;
            red_pts.push((1.05 * angle.cos(), 1.05 * angle.sin()));
        }

        // Left linear transform: affine rotation + shear
        let rot_l = 32.0 * std::f32::consts::PI / 180.0 * transform_p;
        let cos_l = rot_l.cos();
        let sin_l = rot_l.sin();
        let linear_tf = move |u: f32, v: f32| -> (f32, f32) {
            let u1 = u * cos_l - v * sin_l;
            let v1 = u * sin_l + v * cos_l;
            let u2 = u1 + 0.25 * transform_p * v1;
            let v2 = v1 * (1.0 - 0.2 * transform_p);
            (u2, v2)
        };

        // Right non-linear transform: space bending (activation fold)
        // Compressing linear v1 and applying strong radial activation bend 1.35*(r^2 - 0.65)
        // This cleanly pushes all blue points below v2 = -0.3, and all red points above v2 = +0.2!
        let rot_r = 15.0 * std::f32::consts::PI / 180.0 * transform_p;
        let cos_r = rot_r.cos();
        let sin_r = rot_r.sin();
        let nonlinear_tf = move |u: f32, v: f32| -> (f32, f32) {
            let u1 = u * cos_r - v * sin_r;
            let v1 = u * sin_r + v * cos_r;
            let r2 = u1 * u1 + v1 * v1;
            let v_linear = v1 * (1.0 - 0.65 * transform_p);
            let v_bend = transform_p * 1.35 * (r2 - 0.65);
            let u2 = u1;
            let v2 = v_linear + v_bend;
            (u2, v2)
        };

        // Status messages (ASCII-safe text)
        let (left_status_title, left_status_subtitle, left_status_bg, left_status_border, left_status_text_color) =
            if boundary_appear > 0.5 {
                (
                    "ПОМИЛКА: Прямі лінії лишаються прямими — класи нероздільні!",
                    "Скільки б лінійних шарів не додавали, пряма межа ніколи не відокремить вкладені кільця (Колапс у 1 шар)",
                    "#FEE2E2",
                    "#EF4444",
                    "#DC2626",
                )
            } else {
                (
                    "Лінійні шари лише повертають і розтягують координати",
                    "Всі лінії сітки залишаються ідеально прямими та паралельними",
                    "#F8FAFC",
                    "#E2E8F0",
                    "#475569",
                )
            };

        let (right_status_title, right_status_subtitle, right_status_bg, right_status_border, right_status_text_color) =
            if boundary_appear > 0.5 {
                (
                    "УСПІХ: Простір зігнуто! Класи ідеально розділені однією прямою!",
                    "Нелінійна активація розводить внутрішні та зовнішні точки по різні боки межі",
                    "#D1FAE5",
                    "#10B981",
                    "#059669",
                )
            } else {
                (
                    "Функція активації вигинає простір у нелінійну форму",
                    "Лінії координатної сітки вигинаються, змінюючи взаємне розташування точок",
                    "#EFF6FF",
                    "#93C5FD",
                    "#1D4ED8",
                )
            };

        // Progress bar width
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
                    <filter id="shadow-badge" x="-10%" y="-10%" width="120%" height="120%">
                        <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.06" />
                    </filter>

                    // Clipping rectangles for inner canvases to prevent overflow
                    <clipPath id="left-canvas-clip">
                        <rect x="110" y="238" width="780" height="584" rx="14" />
                    </clipPath>
                    <clipPath id="right-canvas-clip">
                        <rect x="1030" y="238" width="780" height="584" rx="14" />
                    </clipPath>
                </defs>

                // Background
                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />

                // Top Header Section
                <g opacity={intro_alpha}>
                    <rect x="80" y="28" width="1760" height="96" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" filter="url(#shadow-card)" />
                    <text x="110" y="68" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN}>
                        "Чому потрібна нелінійність: Деформація простору нейронною мережею"
                    </text>
                    <text x="110" y="100" font-family={FONT} font-size="17" fill={TEXT_MUTED}>
                        "Лінійні шари лише крутять і розтягують сітку • Тільки функція активації згинає простір для розділення класів"
                    </text>

                    // Top Right Highlight Badge
                    <rect x="1450" y="50" width="360" height="50" rx="25" fill={COLOR_AMBER_LIGHT} stroke={COLOR_AMBER} stroke-width="1.5" />
                    <text x="1630" y="81" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">
                        "100 лінійних шарів = 1 персептрон"
                    </text>
                </g>

                // ================= LEFT PANEL (WITHOUT ACTIVATION) =================
                <g opacity={intro_alpha}>
                    <rect x="80" y="144" width="840" height="796" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="2.0" filter="url(#shadow-card)" />

                    // Left Panel Header Badge
                    <rect x="110" y="170" width="780" height="52" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5" />
                    <text x="130" y="202" font-family={FONT} font-size="18" font-weight="700" fill="#B45309">
                        "БЕЗ АКТИВАЦІЇ"
                    </text>
                    <text x="290" y="202" font-family={FONT} font-size="16" fill={TEXT_MUTED}>
                        "y = W2 · (W1 · x + b1) + b2 = W' · x + b'"
                    </text>
                    <rect x="735" y="178" width="140" height="36" rx="18" fill="#FEE2E2" stroke="#EF4444" stroke-width="1.0" />
                    <text x="805" y="201" font-family={FONT} font-size="14" font-weight="700" fill="#DC2626" text-anchor="middle">
                        "Колапс у 1 шар"
                    </text>

                    // Left Grid Canvas Background
                    <rect x="110" y="238" width="780" height="584" rx="14" fill="#FBFDFF" stroke="#E2E8F0" stroke-width="1.5" />

                    // Left Canvas Content Clipped to Box
                    <g clip-path="url(#left-canvas-clip)">
                        // Grid Lines (Left)
                        {
                            (-4..=4).flat_map(|i| {
                                let val = (i as f32) * 0.35;
                                let is_axis = i == 0;
                                let stroke_c = if is_axis { GRID_AXIS_COLOR } else { GRID_LINE_COLOR };
                                let stroke_w = if is_axis { "2.5" } else { "1.2" };

                                let (u1, v1) = linear_tf(-1.5, val);
                                let (u2, v2) = linear_tf(1.5, val);
                                let x1 = left_cx + u1 * scale;
                                let y1 = left_cy - v1 * scale;
                                let x2 = left_cx + u2 * scale;
                                let y2 = left_cy - v2 * scale;

                                let (vu1, vv1) = linear_tf(val, -1.5);
                                let (vu2, vv2) = linear_tf(val, 1.5);
                                let vx1 = left_cx + vu1 * scale;
                                let vy1 = left_cy - vv1 * scale;
                                let vx2 = left_cx + vu2 * scale;
                                let vy2 = left_cy - vv2 * scale;

                                vec![
                                    fframes::svgr!(<line x1={x1} y1={y1} x2={x2} y2={y2} stroke={stroke_c} stroke-width={stroke_w} opacity="0.85" />),
                                    fframes::svgr!(<line x1={vx1} y1={vy1} x2={vx2} y2={vy2} stroke={stroke_c} stroke-width={stroke_w} opacity="0.85" />),
                                ]
                            }).collect::<Vec<_>>()
                        }

                        // Left Failing Boundary Line (t >= 4.5s)
                        {
                            if boundary_appear > 0.01 {
                                let lx1 = left_cx - 260.0;
                                let ly1 = left_cy + 90.0;
                                let lx2 = left_cx + 260.0;
                                let ly2 = left_cy - 90.0;
                                let op = format!("{:.2}", boundary_appear);
                                vec![
                                    fframes::svgr!(
                                        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke="#EF4444" stroke-width="3.5" stroke-dasharray="8,6" opacity={op.clone()} />
                                    ),
                                    fframes::svgr!(
                                        <g opacity={op}>
                                            <circle cx={left_cx} cy={left_cy} r="14" fill="#FFFFFF" stroke="#EF4444" stroke-width="2.5" />
                                            <line x1={left_cx - 7.0} y1={left_cy - 7.0} x2={left_cx + 7.0} y2={left_cy + 7.0} stroke="#EF4444" stroke-width="2.5" />
                                            <line x1={left_cx + 7.0} y1={left_cy - 7.0} x2={left_cx - 7.0} y2={left_cy + 7.0} stroke="#EF4444" stroke-width="2.5" />
                                        </g>
                                    ),
                                ]
                            } else {
                                vec![]
                            }
                        }

                        // Left Points: Blue (inner)
                        {
                            blue_pts.iter().map(|pt| {
                                let (u, v) = linear_tf(pt.0, pt.1);
                                let px = left_cx + u * scale;
                                let py = left_cy - v * scale;
                                fframes::svgr!(
                                    <circle cx={px} cy={py} r="9.5" fill={COLOR_BLUE} stroke="#0F172A" stroke-width="2.2" />
                                )
                            }).collect::<Vec<_>>()
                        }

                        // Left Points: Red (outer)
                        {
                            red_pts.iter().map(|pt| {
                                let (u, v) = linear_tf(pt.0, pt.1);
                                let px = left_cx + u * scale;
                                let py = left_cy - v * scale;
                                fframes::svgr!(
                                    <circle cx={px} cy={py} r="9.5" fill={COLOR_RED} stroke="#0F172A" stroke-width="2.2" />
                                )
                            }).collect::<Vec<_>>()
                        }
                    </g>

                    // Left Panel Status Footer
                    <rect x="110" y="838" width="780" height="84" rx="14" fill={left_status_bg} stroke={left_status_border} stroke-width="1.5" />
                    <text x="500" y="872" font-family={FONT} font-size="17" font-weight="700" fill={left_status_text_color} text-anchor="middle">
                        {left_status_title}
                    </text>
                    <text x="500" y="900" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        {left_status_subtitle}
                    </text>
                </g>

                // ================= RIGHT PANEL (WITH ACTIVATION) =================
                <g opacity={intro_alpha}>
                    <rect x="1000" y="144" width="840" height="796" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="2.0" filter="url(#shadow-card)" />

                    // Right Panel Header Badge
                    <rect x="1030" y="170" width="780" height="52" rx="12" fill={COLOR_BLUE_LIGHT} stroke="#BFDBFE" stroke-width="1.5" />
                    <text x="1050" y="202" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_BLUE}>
                        "З ФУНКЦІЄЮ АКТИВАЦІЇ"
                    </text>
                    <text x="1300" y="202" font-family={FONT} font-size="16" fill={TEXT_MUTED}>
                        "y = σ( W2 · σ(W1 · x + b1) + b2 )"
                    </text>
                    <rect x="1665" y="178" width="130" height="36" rx="18" fill={COLOR_GREEN_LIGHT} stroke={COLOR_GREEN} stroke-width="1.0" />
                    <text x="1730" y="201" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                        "Вигин простору"
                    </text>

                    // Right Grid Canvas Background
                    <rect x="1030" y="238" width="780" height="584" rx="14" fill="#FBFDFF" stroke="#E2E8F0" stroke-width="1.5" />

                    // Right Canvas Content Clipped to Box
                    <g clip-path="url(#right-canvas-clip)">
                        // Curved Grid Paths (Right)
                        {
                            (-4..=4).flat_map(|i| {
                                let val = (i as f32) * 0.35;
                                let is_axis = i == 0;
                                let stroke_c = if is_axis { GRID_AXIS_COLOR } else { GRID_LINE_COLOR };
                                let stroke_w = if is_axis { "2.5" } else { "1.2" };

                                // Sample horizontal path
                                let mut d_h = String::with_capacity(256);
                                for step in 0..=30 {
                                    let u = -1.5 + (step as f32) * 3.0 / 30.0;
                                    let (tu, tv) = nonlinear_tf(u, val);
                                    let px = right_cx + tu * scale;
                                    let py = right_cy - tv * scale;
                                    if step == 0 {
                                        d_h.push_str(&format!("M {:.1} {:.1}", px, py));
                                    } else {
                                        d_h.push_str(&format!(" L {:.1} {:.1}", px, py));
                                    }
                                }

                                // Sample vertical path
                                let mut d_v = String::with_capacity(256);
                                for step in 0..=30 {
                                    let v = -1.5 + (step as f32) * 3.0 / 30.0;
                                    let (tu, tv) = nonlinear_tf(val, v);
                                    let px = right_cx + tu * scale;
                                    let py = right_cy - tv * scale;
                                    if step == 0 {
                                        d_v.push_str(&format!("M {:.1} {:.1}", px, py));
                                    } else {
                                        d_v.push_str(&format!(" L {:.1} {:.1}", px, py));
                                    }
                                }

                                vec![
                                    fframes::svgr!(<path d={d_h} fill="none" stroke={stroke_c} stroke-width={stroke_w} opacity="0.85" />),
                                    fframes::svgr!(<path d={d_v} fill="none" stroke={stroke_c} stroke-width={stroke_w} opacity="0.85" />),
                                ]
                            }).collect::<Vec<_>>()
                        }

                        // Right Clean Separating Line (t >= 4.5s)
                        // All blue points are below cy - (-0.5)*scale = cy + 80
                        // All red points are above cy - (+0.4)*scale = cy - 64
                        // So the separating line at cy + 10 cleanly splits them with a huge 140px margin!
                        {
                            if boundary_appear > 0.01 {
                                let rx1 = right_cx - 360.0;
                                let ry = right_cy + 12.0;
                                let rx2 = right_cx + 360.0;
                                let op = format!("{:.2}", boundary_appear);
                                let bg_op = format!("{:.2}", 0.28 * boundary_appear);

                                vec![
                                    fframes::svgr!(
                                        <rect x={right_cx - 390.0} y={ry} width="780" height="270" fill={COLOR_BLUE_LIGHT} opacity={bg_op} />
                                    ),
                                    fframes::svgr!(
                                        <line x1={rx1} y1={ry} x2={rx2} y2={ry} stroke={COLOR_GREEN} stroke-width="4.0" opacity={op.clone()} />
                                    ),
                                    fframes::svgr!(
                                        <g opacity={op}>
                                            <rect x={right_cx + 100.0} y={ry - 32.0} width="220" height="28" rx="6" fill="#FFFFFF" stroke={COLOR_GREEN} stroke-width="1.5" />
                                            <text x={right_cx + 210.0} y={ry - 13.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_GREEN} text-anchor="middle">
                                                "Лінійна межа: w·h + b = 0"
                                            </text>
                                        </g>
                                    ),
                                ]
                            } else {
                                vec![]
                            }
                        }

                        // Right Points: Blue (inner)
                        {
                            blue_pts.iter().map(|pt| {
                                let (u, v) = nonlinear_tf(pt.0, pt.1);
                                let px = right_cx + u * scale;
                                let py = right_cy - v * scale;
                                fframes::svgr!(
                                    <circle cx={px} cy={py} r="9.5" fill={COLOR_BLUE} stroke="#0F172A" stroke-width="2.2" />
                                )
                            }).collect::<Vec<_>>()
                        }

                        // Right Points: Red (outer)
                        {
                            red_pts.iter().map(|pt| {
                                let (u, v) = nonlinear_tf(pt.0, pt.1);
                                let px = right_cx + u * scale;
                                let py = right_cy - v * scale;
                                fframes::svgr!(
                                    <circle cx={px} cy={py} r="9.5" fill={COLOR_RED} stroke="#0F172A" stroke-width="2.2" />
                                )
                            }).collect::<Vec<_>>()
                        }
                    </g>

                    // Right Panel Status Footer
                    <rect x="1030" y="838" width="780" height="84" rx="14" fill={right_status_bg} stroke={right_status_border} stroke-width="1.5" />
                    <text x="1420" y="872" font-family={FONT} font-size="17" font-weight="700" fill={right_status_text_color} text-anchor="middle">
                        {right_status_title}
                    </text>
                    <text x="1420" y="900" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        {right_status_subtitle}
                    </text>
                </g>

                // ================= BOTTOM TIMELINE & LEGEND =================
                <g opacity={intro_alpha}>
                    <circle cx="120" cy="970" r="8.5" fill={COLOR_BLUE} stroke="#0F172A" stroke-width="2.0" />
                    <text x="140" y="976" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                        "Клас 1 (Центральні точки)"
                    </text>

                    <circle cx="410" cy="970" r="8.5" fill={COLOR_RED} stroke="#0F172A" stroke-width="2.0" />
                    <text x="430" y="976" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                        "Клас 0 (Зовнішнє кільце)"
                    </text>

                    <line x1="720" y1="970" x2="760" y2="970" stroke={COLOR_GREEN} stroke-width="3.5" />
                    <text x="775" y="976" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_GREEN}>
                        "Роздільна пряма лінія вихідного нейрона"
                    </text>

                    <text x="1840" y="976" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED} text-anchor="end">
                        "kostyl.dev • Інженерний практикум з нейромереж"
                    </text>

                    // Progress Bar
                    <rect x="80" y="1000" width={bar_width} height="6" rx="3" fill="#E2E8F0" />
                    <rect x="80" y="1000" width={progress_w} height="6" rx="3" fill={COLOR_BLUE} />
                </g>
            </svg>
        )
    }
}
