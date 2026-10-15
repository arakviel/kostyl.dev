//! XOR Failure visualization using fframes.
//!
//! Renders an animated proof of why a single linear decision boundary
//! w1*x1 + w2*x2 + b = 0 can NEVER separate the XOR function.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct XorMedia, "media");

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
const COLOR_RED_LIGHT: &str = "#FEF2F2";
const COLOR_GREEN: &str = "#059669";
const COLOR_GREEN_LIGHT: &str = "#ECFDF5";
const COLOR_AMBER: &str = "#D97706";
const COLOR_AMBER_LIGHT: &str = "#FEF3C7";
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

pub struct XorVideo<'a> {
    pub media: &'a XorMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> XorVideo<'a> {
    pub fn new(media: &'a XorMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for XorVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("XorVideo").finish()
    }
}

impl fframes::Video for XorVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(255, 255, 255);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.0)..AudioTimestamp::Eof).gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.0)..AudioTimestamp::Eof).gain_db(-3.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(7.5)..AudioTimestamp::Eof).gain_db(0.0),
        ])
    }

    fn render_frame<'a>(&'a self, frame: Frame, _ctx: &FFramesContext<'a, '_>) -> Svgr<'a> {
        let t = frame.seconds();
        let intro_alpha = ease_out_cubic(clamp(t / 0.8, 0.0, 1.0));

        // Coordinate plot setup
        let plot_cx = 580.0_f32;
        let plot_cy = 580.0_f32;
        let plot_scale = 360.0_f32; // 360px per 1.0 unit

        // Screen mapping: (x1, x2) in [0..1]
        let to_screen = |x1: f32, x2: f32| -> (f32, f32) {
            let px = plot_cx + (x1 - 0.5) * plot_scale;
            let py = plot_cy - (x2 - 0.5) * plot_scale;
            (px, py)
        };

        // Rotation angle of the separating line:
        // Rotates smoothly from 0 to 360 degrees across the 10s video
        let angle_deg = (t / 10.0) * 360.0;
        let angle_rad = angle_deg * std::f32::consts::PI / 180.0;

        // Line defined as: cos(a)*(x1 - 0.5) + sin(a)*(x2 - 0.5) = offset
        // Offset oscillates slightly to test parallel cuts
        let offset = 0.18 * ((t * 1.5).sin());
        let normal_x = angle_rad.cos();
        let normal_y = angle_rad.sin();

        // 4 XOR points: (x1, x2, label, expected_class)
        let pts = [
            (0.0_f32, 0.0_f32, "(0, 0)", 0),
            (0.0_f32, 1.0_f32, "(0, 1)", 1),
            (1.0_f32, 0.0_f32, "(1, 0)", 1),
            (1.0_f32, 1.0_f32, "(1, 1)", 0),
        ];

        // Evaluate predictions:
        // side = normal_x * (x1 - 0.5) + normal_y * (x2 - 0.5) - offset
        // pred = if side >= 0 { 1 } else { 0 }
        let mut error_count = 0;
        let mut results = Vec::new();

        for (x1, x2, name, target) in pts.iter() {
            let val = normal_x * (x1 - 0.5) + normal_y * (x2 - 0.5) - offset;
            let pred = if val >= 0.0 { 1 } else { 0 };
            let ok = pred == *target;
            if !ok {
                error_count += 1;
            }
            results.push((*name, *target, pred, ok, val));
        }

        // Compute line endpoints across the canvas box
        let dir_x = -normal_y;
        let dir_y = normal_x;
        let line_len = 540.0_f32;

        let center_x = plot_cx + normal_x * offset * plot_scale;
        let center_y = plot_cy - normal_y * offset * plot_scale;

        let lx1 = center_x - dir_x * line_len;
        let ly1 = center_y + dir_y * line_len;
        let lx2 = center_x + dir_x * line_len;
        let ly2 = center_y - dir_y * line_len;

        // Progress bar
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
                    <filter id="shadow-node" x="-15%" y="-15%" width="130%" height="130%">
                        <feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#0F172A" flood-opacity="0.10" />
                    </filter>

                    <clipPath id="plot-clip">
                        <rect x="110" y="238" width="940" height="686" rx="14" />
                    </clipPath>
                </defs>

                // Background
                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />

                // TOP HEADER
                <g opacity={intro_alpha}>
                    <rect x="80" y="28" width="1760" height="96" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" filter="url(#shadow-card)" />
                    <text x="110" y="68" font-family={FONT} font-size="28" font-weight="700" fill={TEXT_MAIN}>
                        "Проблема XOR: Межа лінійної роздільності персептрона"
                    </text>
                    <text x="110" y="100" font-family={FONT} font-size="17" fill={TEXT_MUTED}>
                        "Пряма лінія w1·x1 + w2·x2 + b = 0 безперервно обертається, але жодна пряма не здатна розділити класи XOR"
                    </text>

                    // Top Badge
                    <rect x="1460" y="50" width="350" height="50" rx="25" fill={COLOR_RED_LIGHT} stroke={COLOR_RED} stroke-width="1.5" />
                    <text x="1635" y="81" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_RED} text-anchor="middle">
                        "100% точність неможлива!"
                    </text>
                </g>

                // ================= LEFT: 2D PLOT & ROTATING LINE =================
                <g opacity={intro_alpha}>
                    // Main Plot Frame
                    <rect x="80" y="144" width="1000" height="804" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="2.0" filter="url(#shadow-card)" />

                    // Plot Header Badge
                    <rect x="110" y="170" width="940" height="50" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5" />
                    <text x="135" y="202" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_AMBER}>
                        "ВХІДНИЙ ПРОСТІР (x1, x2)"
                    </text>
                    <text x="420" y="202" font-family={FONT} font-size="16" fill={TEXT_MUTED}>
                        {format!("Кут нахилу межі: {:.0}° • Зсув: {:.2}", angle_deg, offset)}
                    </text>

                    // Clipped Plot Content
                    <g clip-path="url(#plot-clip)">
                        // Canvas Background
                        <rect x="110" y="238" width="940" height="686" rx="14" fill="#FAFCFF" />

                        // Coordinate Axes
                        {
                            let (ax0_x, ax0_y) = to_screen(0.0, 0.0);
                            let (ax1_x, _ax1_y) = to_screen(1.3, 0.0);
                            let (_ax2_x, ax2_y) = to_screen(0.0, 1.3);
                            vec![
                                fframes::svgr!(<line x1={ax0_x - 60.0} y1={ax0_y} x2={ax1_x} y2={ax0_y} stroke={GRID_AXIS_COLOR} stroke-width="2.0" />),
                                fframes::svgr!(<line x1={ax0_x} y1={ax0_y + 60.0} x2={ax0_x} y2={ax2_y} stroke={GRID_AXIS_COLOR} stroke-width="2.0" />),
                            ]
                        }

                        // Grid tick marks and labels
                        {
                            (1..=2).flat_map(|i| {
                                let v = i as f32 * 0.5;
                                let (gx, gy) = to_screen(v, v);
                                let (x_zero, y_zero) = to_screen(0.0, 0.0);
                                vec![
                                    fframes::svgr!(<line x1={gx} y1={y_zero - 6.0} x2={gx} y2={y_zero + 6.0} stroke={GRID_AXIS_COLOR} stroke-width="2.0" />),
                                    fframes::svgr!(<text x={gx} y={y_zero + 28.0} font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED} text-anchor="middle">{format!("{:.1}", v)}</text>),
                                    fframes::svgr!(<line x1={x_zero - 6.0} y1={gy} x2={x_zero + 6.0} y2={gy} stroke={GRID_AXIS_COLOR} stroke-width="2.0" />),
                                    fframes::svgr!(<text x={x_zero - 18.0} y={gy + 5.0} font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED} text-anchor="end">{format!("{:.1}", v)}</text>),
                                ]
                            }).collect::<Vec<_>>()
                        }

                        // Rotating Linear Boundary Line
                        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke={COLOR_AMBER} stroke-width="5.0" />
                        <line x1={lx1} y1={ly1} x2={lx2} y2={ly2} stroke="#FFFFFF" stroke-width="2.0" stroke-dasharray="8,8" />

                        // Center Pivot point
                        <circle cx={center_x} cy={center_y} r="6" fill={COLOR_AMBER} stroke="#0F172A" stroke-width="2" />

                        // 4 XOR Points
                        {
                            pts.iter().map(|(x1, x2, label, cls)| {
                                let (sx, sy) = to_screen(*x1, *x2);
                                let color = if *cls == 1 { COLOR_BLUE } else { COLOR_RED };
                                let (lbl_dx, lbl_dy) = match (*x1 as i32, *x2 as i32) {
                                    (0, 0) => (-30.0, 36.0),
                                    (0, 1) => (-30.0, -22.0),
                                    (1, 0) => (30.0, 36.0),
                                    _ => (30.0, -22.0),
                                };

                                fframes::svgr!(
                                    <g filter="url(#shadow-node)">
                                        <circle cx={sx} cy={sy} r="20" fill={color} stroke="#0F172A" stroke-width="3.5" />
                                        <circle cx={sx} cy={sy} r="7" fill="#FFFFFF" />
                                        <rect x={sx + lbl_dx - 32.0} y={sy + lbl_dy - 16.0} width="64" height="26" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
                                        <text x={sx + lbl_dx} y={sy + lbl_dy + 2.0} font-family={FONT} font-size="13" font-weight="700" fill={color} text-anchor="middle">
                                            {*label}
                                        </text>
                                    </g>
                                )
                            }).collect::<Vec<_>>()
                        }
                    </g>
                </g>

                // ================= RIGHT: LIVE EVALUATION DASHBOARD =================
                <g opacity={intro_alpha}>
                    <rect x="1110" y="144" width="730" height="804" rx="20" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="2.0" filter="url(#shadow-card)" />

                    // Live Status Header
                    <rect x="1140" y="170" width="670" height="50" rx="12" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1.5" />
                    <text x="1165" y="202" font-family={FONT} font-size="18" font-weight="700" fill={TEXT_MAIN}>
                        "АНАЛІЗ РОЗДІЛЕННЯ В РЕАЛЬНОМУ ЧАСІ"
                    </text>

                    // Big Error Metric Card
                    <rect x="1140" y="238" width="670" height="150" rx="16" fill={COLOR_RED_LIGHT} stroke="#FCA5A5" stroke-width="1.5" />
                    <text x="1170" y="278" font-family={FONT} font-size="16" font-weight="700" fill="#991B1B">
                        "ПОТОЧНИЙ СТАН РОЗДІЛЕННЯ:"
                    </text>
                    <text x="1170" y="325" font-family={FONT} font-size="34" font-weight="700" fill={COLOR_RED}>
                        {format!("Помилок: {} з 4 точок", error_count)}
                    </text>
                    <text x="1170" y="362" font-family={FONT} font-size="17" font-weight="700" fill="#B91C1C">
                        {format!("Максимальна точність: {:.0}% • Потрібно 100%", (4 - error_count) as f32 / 4.0 * 100.0)}
                    </text>

                    // Evaluation Table Header
                    <rect x="1140" y="410" width="670" height="42" rx="8" fill="#F1F5F9" />
                    <text x="1165" y="437" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED}>"Точка"</text>
                    <text x="1275" y="437" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED}>"Очікується"</text>
                    <text x="1405" y="437" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED}>"Розпізнано"</text>
                    <text x="1560" y="437" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED}>"Статус"</text>

                    // Evaluation Rows
                    {
                        results.iter().enumerate().map(|(idx, (name, target, pred, ok, _val))| {
                            let ry = 465.0 + (idx as f32) * 60.0;
                            let row_bg = if *ok { COLOR_GREEN_LIGHT } else { COLOR_RED_LIGHT };
                            let row_border = if *ok { "#86EFAC" } else { "#FECACA" };
                            let status_text = if *ok { "[OK] Вірно" } else { "[X] Помилка" };
                            let status_color = if *ok { COLOR_GREEN } else { COLOR_RED };

                            fframes::svgr!(
                                <g>
                                    <rect x="1140" y={ry} width="670" height="52" rx="10" fill={row_bg} stroke={row_border} stroke-width="1.2" />
                                    <text x="1165" y={ry + 32.0} font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                                        {*name}
                                    </text>
                                    <text x="1295" y={ry + 32.0} font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                                        {format!("Клас {}", target)}
                                    </text>
                                    <text x="1425" y={ry + 32.0} font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                                        {format!("Клас {}", pred)}
                                    </text>
                                    <rect x="1540" y={ry + 11.0} width="120" height="30" rx="6" fill="#FFFFFF" stroke={status_color} stroke-width="1.0" />
                                    <text x="1600" y={ry + 31.0} font-family={FONT} font-size="13" font-weight="700" fill={status_color} text-anchor="middle">
                                        {status_text}
                                    </text>
                                </g>
                            )
                        }).collect::<Vec<_>>()
                    }

                    // Key Conclusion Box at Bottom Right
                    <rect x="1140" y="730" width="670" height="188" rx="16" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1.5" />
                    <text x="1170" y="768" font-family={FONT} font-size="18" font-weight="700" fill="#92400E">
                        "Чому це глухий кут для 1 персептрона:"
                    </text>
                    <text x="1170" y="802" font-family={FONT} font-size="15" fill="#78350F">
                        "• Класи XOR розташовані по діагоналях: (0,0) і (1,1) проти (0,1) і (1,0)"
                    </text>
                    <text x="1170" y="832" font-family={FONT} font-size="15" fill="#78350F">
                        "• Будь-яка пряма лінія відтинає максимум одну пару точок"
                    </text>
                    <text x="1170" y="862" font-family={FONT} font-size="15" font-weight="700" fill="#B45309">
                        "• Висновок: для розв'язання XOR необхідно мінімум ДВІ прямі (MLP)"
                    </text>
                </g>

                // ================= FOOTER =================
                <g opacity={intro_alpha}>
                    <circle cx="120" cy="975" r="8.5" fill={COLOR_BLUE} stroke="#0F172A" stroke-width="2.0" />
                    <text x="140" y="981" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                        "Клас 1: точки (0,1) та (1,0)"
                    </text>

                    <circle cx="410" cy="975" r="8.5" fill={COLOR_RED} stroke="#0F172A" stroke-width="2.0" />
                    <text x="430" y="981" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN}>
                        "Клас 0: точки (0,0) та (1,1)"
                    </text>

                    <line x1="720" y1="975" x2="760" y2="975" stroke={COLOR_AMBER} stroke-width="3.5" />
                    <text x="775" y="981" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_AMBER}>
                        "Поточна роздільна пряма персептрона"
                    </text>

                    <text x="1840" y="981" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MUTED} text-anchor="end">
                        "kostyl.dev • Інженерний практикум з нейромереж"
                    </text>

                    // Progress Bar
                    <rect x="80" y="1005" width={bar_width} height="6" rx="3" fill="#E2E8F0" />
                    <rect x="80" y="1005" width={progress_w} height="6" rx="3" fill={COLOR_AMBER} />
                </g>
            </svg>
        )
    }
}
