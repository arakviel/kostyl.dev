//! Gradient & Optimization Geometric Intuition visualization using fframes.
//!
//! Visualizes gradient concepts across 1D loss bowl and 2D contour maps:
//! 1. 1D Bowl: Loss curve L(w), tangent line, gradient vector (pointing up) vs descent step (pointing down).
//! 2. Steep vs Flat: Magnitude of gradient |grad L| determines step size; large on steep slopes, small near minimum.
//! 3. 2D Contour Map: Loss isolines L(w1, w2) with orthogonal gradient vectors guiding optimization to global minimum.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct GradMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

// Kostyl Dark Theme Palette
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

pub struct GradVideo<'a> {
    pub media: &'a GradMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> GradVideo<'a> {
    pub fn new(media: &'a GradMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for GradVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GradVideo").finish()
    }
}

impl fframes::Video for GradVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.2)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(2.3)..AudioTimestamp::Eof).gain_db(0.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(3.6)..AudioTimestamp::Eof).gain_db(-3.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(4.7)..AudioTimestamp::Eof).gain_db(-1.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(7.2)..AudioTimestamp::Eof).gain_db(1.0),
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

        // Continuous optimization timeline across 3 steps:
        // Initial state: w = 2.40
        // Step 1: 1.8s -> 2.6s (w: 2.40 -> 1.20)
        // Step 2: 4.0s -> 4.8s (w: 1.20 -> 0.40)
        // Step 3: 6.2s -> 7.0s (w: 0.40 -> 0.02)
        let w_val = if t < 1.8 {
            2.40
        } else if t < 2.6 {
            let p = ease_in_out((t - 1.8) / 0.8);
            2.40 - 1.20 * p
        } else if t < 4.0 {
            1.20
        } else if t < 4.8 {
            let p = ease_in_out((t - 4.0) / 0.8);
            1.20 - 0.80 * p
        } else if t < 6.2 {
            0.40
        } else if t < 7.0 {
            let p = ease_in_out((t - 6.2) / 0.8);
            0.40 - 0.38 * p
        } else {
            0.02
        };

        // 1D Parabola Geometry:
        // Center x0 = 502, y0 = 740. Scale X: 130px per unit w.
        // L(w) = 0.5 * a * w^2. Scale Y: 60px per unit loss.
        let bowl_cx = 502.0;
        let bowl_cy = 735.0;
        let scale_x = 130.0;
        let scale_y = 62.0;

        let ball_1d_x = bowl_cx + w_val * scale_x;
        let loss_val = 0.5 * w_val * w_val;
        let ball_1d_y = bowl_cy - loss_val * scale_y;

        // Gradient in 1D: dL/dw = w
        let grad_1d = w_val;
        let slope_angle = grad_1d.atan(); // tangent angle in mathematical coordinates

        // Tangent unit vector pointing uphill (right and up):
        let tan_dx = slope_angle.cos();
        let tan_dy = -slope_angle.sin();

        // Arrow lengths based on gradient magnitude
        let grad_arrow_len = clamp(grad_1d.abs() * 55.0, 0.0, 135.0);
        let step_arrow_len = clamp(grad_1d.abs() * 45.0, 0.0, 105.0);

        // Uphill gradient vector tip:
        let grad_tip_x = ball_1d_x + tan_dx * grad_arrow_len;
        let grad_tip_y = ball_1d_y + tan_dy * grad_arrow_len;

        // Downhill descent vector tip:
        let desc_tip_x = ball_1d_x - tan_dx * step_arrow_len;
        let desc_tip_y = ball_1d_y - tan_dy * step_arrow_len;

        // Tangent line endpoints across ball:
        let tan_line_len = 160.0;
        let tan_p1_x = ball_1d_x - tan_dx * tan_line_len;
        let tan_p1_y = ball_1d_y - tan_dy * tan_line_len;
        let tan_p2_x = ball_1d_x + tan_dx * tan_line_len;
        let tan_p2_y = ball_1d_y + tan_dy * tan_line_len;

        // 2D Contour Geometry:
        // Center (1417, 530). Ellipse axes: rx = ry * 1.5.
        let c2_cx = 1417.0;
        let c2_cy = 530.0;

        // In 2D: w1 = w_val, w2 = w_val * 0.75
        let w1_val = w_val;
        let w2_val = w_val * 0.75;
        let pt2_x = c2_cx + w1_val * 115.0;
        let pt2_y = c2_cy - w2_val * 105.0;

        // 2D gradient is perpendicular to contour ellipse.
        let grad2_x = w1_val * 1.1;
        let grad2_y = w2_val * 1.4;
        let grad2_mag = (grad2_x * grad2_x + grad2_y * grad2_y).sqrt();
        let (u_grad2_x, u_grad2_y) = if grad2_mag > 0.001 {
            (grad2_x / grad2_mag, grad2_y / grad2_mag)
        } else {
            (0.0, 0.0)
        };

        let grad2_arrow_len = clamp(grad2_mag * 52.0, 0.0, 125.0);
        let desc2_arrow_len = clamp(grad2_mag * 44.0, 0.0, 100.0);

        // 2D arrows (screen y inverted for y component):
        let pt2_grad_tip_x = pt2_x + u_grad2_x * grad2_arrow_len;
        let pt2_grad_tip_y = pt2_y - u_grad2_y * grad2_arrow_len;

        let pt2_desc_tip_x = pt2_x - u_grad2_x * desc2_arrow_len;
        let pt2_desc_tip_y = pt2_y + u_grad2_y * desc2_arrow_len;

        // Orthogonal tangent on contour:
        let tan2_x = -u_grad2_y;
        let tan2_y = u_grad2_x;
        let tan2_len = 70.0;
        let c_tan1_x = pt2_x - tan2_x * tan2_len;
        let c_tan1_y = pt2_y + tan2_y * tan2_len;
        let c_tan2_x = pt2_x + tan2_x * tan2_len;
        let c_tan2_y = pt2_y - tan2_y * tan2_len;

        // Right angle marker for orthogonality (size = 14px)
        let ra_s = 14.0;
        let ra_p1_x = pt2_x + u_grad2_x * ra_s;
        let ra_p1_y = pt2_y - u_grad2_y * ra_s;
        let ra_p2_x = ra_p1_x + tan2_x * ra_s;
        let ra_p2_y = ra_p1_y - tan2_y * ra_s;
        let ra_p3_x = pt2_x + tan2_x * ra_s;
        let ra_p3_y = pt2_y - tan2_y * ra_s;

        // Active Phase Descriptions:
        let (phase_badge, phase_slope_text, phase_lr_text) = if t < 3.0 {
            (
                "ФАЗА 1: КРУТИЙ СХИЛ (ВЕЛИКИЙ ГРАДІЄНТ)",
                "Крутизна висока (|grad L| = 2.40): дотична різко піднята. Оптимізатор робить великий рішучий крок вниз.",
                "Крок: Δw = -η·(grad L) = -0.25 × 2.40 = -0.60"
            )
        } else if t < 6.0 {
            (
                "ФАЗА 2: ПОЛОГИЙ СХИЛ (ТОЧНЕ ДООПРАЦЮВАННЯ)",
                "Крутизна помірна (|grad L| = 1.20): нахил зменшується, вектор скорочується, крок стає обережнішим.",
                "Крок: Δw = -η·(grad L) = -0.25 × 1.20 = -0.30"
            )
        } else if t < 8.2 {
            (
                "ФАЗА 3: ТОЧКА МІНІМУМУ (РІВНОВАГА grad L ≈ 0)",
                "Дно чаші досягнуто: дотична горизонтальна, похідна дорівнює нулю. Рух зупиняється без перелітання.",
                "Рівновага: grad L = 0.00 -> Δw = 0.00 (Оптимум знайдено)"
            )
        } else {
            (
                "ФАЗА 4: ЗАВЕРШЕННЯ ОПТИМІЗАЦІЇ",
                "Мережа успішно зійшлася до глобального мінімуму функції втрат.",
                "Loss: L(w) ≈ 0.000 (Точність максимальна)"
            )
        };

        // Minimum convergence glow pulse
        let min_glow_opacity = if t >= 6.8 {
            let p = ((t - 6.8) * 4.0).sin().abs();
            (0.3 + 0.4 * p) * loop_reset
        } else {
            0.0
        };

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <radialGradient id="bg-glow" cx="0.5" cy="0.45" r="0.6">
                        <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.35" />
                        <stop offset="60%" stop-color="#0b1329" stop-opacity="0.10" />
                        <stop offset="100%" stop-color={BG_COLOR} stop-opacity="0" />
                    </radialGradient>

                    <radialGradient id="glow-rose" cx="0.5" cy="0.5" r="0.5">
                        <stop offset="0%" stop-color={COLOR_ROSE} stop-opacity="0.6" />
                        <stop offset="100%" stop-color={COLOR_ROSE} stop-opacity="0" />
                    </radialGradient>

                    <radialGradient id="glow-emerald" cx="0.5" cy="0.5" r="0.5">
                        <stop offset="0%" stop-color={COLOR_EMERALD} stop-opacity="0.7" />
                        <stop offset="100%" stop-color={COLOR_EMERALD} stop-opacity="0" />
                    </radialGradient>

                    <pattern id="dot-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="1.2" fill="#334155" opacity="0.25" />
                    </pattern>

                    <marker id="arrow-rose" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill={COLOR_ROSE} />
                    </marker>
                    <marker id="arrow-emerald" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill={COLOR_EMERALD} />
                    </marker>
                    <marker id="arrow-cyan" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
                        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill={COLOR_CYAN} />
                    </marker>
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH / 2} cy={HEIGHT / 2} r="800" fill="url(#bg-glow)" />

                <g opacity={intro_alpha * loop_reset}>
                    <rect x="730" y="24" width="460" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "МАТЕМАТИЧНА ІНТУЇЦІЯ: ВЕКТОРНИЙ АНАЛІЗ & AUTOGRAD"
                    </text>

                    <text x="960" y="92" font-family={FONT} font-size="32" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Що таке градієнт: Напрямок, Крутизна та Крок Оптимізації"
                    </text>

                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "Градієнт (+grad L) показує найкрутіший підйом вгору. Оптимізатор крокує у протилежний бік: w_new = w - η·(grad L)"
                    </text>
                </g>

                <g opacity={intro_alpha * loop_reset}>
                    <rect x="70" y="155" width="875" height="695" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />

                    <rect x="95" y="175" width="460" height="30" rx="8" fill="#1e293b" />
                    <text x="110" y="195" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">
                        "1D: КРИВА ВТРАТ L(w) ТА ДОТИЧНА (КРУТИЗНА НАХИЛУ)"
                    </text>

                    <line x1="130" y1={bowl_cy} x2="880" y2={bowl_cy} stroke="#334155" stroke-width="1.5" stroke-dasharray="4 4" />
                    <line x1={bowl_cx} y1="230" x2={bowl_cx} y2={bowl_cy + 25.0} stroke="#334155" stroke-width="1.5" stroke-dasharray="4 4" />
                    <text x="890" y={bowl_cy + 5.0} font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"Параметр w"</text>
                    <text x={bowl_cx + 10.0} y="245" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"Втрати L(w)"</text>

                    <path
                        d="M 151 514 Q 502 966 853 514"
                        fill="none"
                        stroke="#0284c7"
                        stroke-width="3.5"
                    />

                    <path
                        d={format!("M {:.1} {:.1} Q 502 966 {:.1} {:.1}", bowl_cx + 2.40 * scale_x, bowl_cy - 0.5 * 2.40 * 2.40 * scale_y, ball_1d_x, ball_1d_y)}
                        fill="none"
                        stroke={COLOR_EMERALD}
                        stroke-width="4.0"
                        stroke-dasharray="4 4"
                        opacity="0.5"
                    />

                    <circle cx={bowl_cx} cy={bowl_cy} r="6" fill={COLOR_EMERALD} />
                    <circle cx={bowl_cx} cy={bowl_cy} r="18" fill={COLOR_EMERALD} opacity={format!("{:.2}", min_glow_opacity)} />
                    <text x={bowl_cx} y={bowl_cy + 34.0} font-family={FONT} font-size="12" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                        "Мінімум L(w) = 0 (grad L = 0)"
                    </text>

                    <line
                        x1={tan_p1_x}
                        y1={tan_p1_y}
                        x2={tan_p2_x}
                        y2={tan_p2_y}
                        stroke="#94a3b8"
                        stroke-width="2"
                        stroke-dasharray="6 4"
                        opacity="0.85"
                    />

                    {
                        if grad_arrow_len > 12.0 {
                            fframes::svgr!(
                                <g>
                                    <line
                                        x1={ball_1d_x}
                                        y1={ball_1d_y}
                                        x2={grad_tip_x}
                                        y2={grad_tip_y}
                                        stroke={COLOR_ROSE}
                                        stroke-width="4.0"
                                        stroke-linecap="round"
                                        marker-end="url(#arrow-rose)"
                                    />
                                    <text
                                        x={grad_tip_x + 12.0}
                                        y={grad_tip_y - 6.0}
                                        font-family={FONT}
                                        font-size="14"
                                        font-weight="700"
                                        fill={COLOR_ROSE}
                                    >
                                        {format!("+grad L = +{:.2} (Підйом)", grad_1d)}
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    {
                        if step_arrow_len > 12.0 {
                            fframes::svgr!(
                                <g>
                                    <line
                                        x1={ball_1d_x}
                                        y1={ball_1d_y}
                                        x2={desc_tip_x}
                                        y2={desc_tip_y}
                                        stroke={COLOR_EMERALD}
                                        stroke-width="4.5"
                                        stroke-linecap="round"
                                        marker-end="url(#arrow-emerald)"
                                    />
                                    <text
                                        x={desc_tip_x - 14.0}
                                        y={desc_tip_y - 12.0}
                                        font-family={FONT}
                                        font-size="13"
                                        font-weight="700"
                                        fill={COLOR_EMERALD}
                                        text-anchor="end"
                                    >
                                        {format!("-η·(grad L) = -{:.2} (Спуск)", grad_1d * 0.25)}
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    <circle cx={ball_1d_x} cy={ball_1d_y} r="22" fill="url(#glow-emerald)" opacity="0.6" />
                    <circle cx={ball_1d_x} cy={ball_1d_y} r="10" fill={TEXT_MAIN} stroke={COLOR_CYAN} stroke-width="3" />

                    <rect x={ball_1d_x - 65.0} y={ball_1d_y - 48.0} width="130" height="26" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1" />
                    <text x={ball_1d_x} y={ball_1d_y - 31.0} font-family={FONT} font-size="12" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        {format!("w = {:.2} | L = {:.2}", w_val, loss_val)}
                    </text>

                    <g transform="translate(100, 775)">
                        <circle cx="15" cy="15" r="6" fill={COLOR_ROSE} />
                        <text x="30" y="19" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_ROSE}>
                            "Червона стрілка (+grad L): Напрямок найкрутішого зростання втрат вгору"
                        </text>

                        <circle cx="15" cy="42" r="6" fill={COLOR_EMERALD} />
                        <text x="30" y="46" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD}>
                            "Зелена стрілка (-η·grad L): Напрямок спуску та величина кроку оновлення ваги"
                        </text>
                    </g>
                </g>

                <g opacity={intro_alpha * loop_reset}>
                    <rect x="975" y="155" width="875" height="695" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />

                    <rect x="1000" y="175" width="530" height="30" rx="8" fill="#1e293b" />
                    <text x="1015" y="195" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">
                        "2D: ТОПОГРАФІЧНІ ІЗОЛІНІЇ L(w1, w2) & ОРТОГОНАЛЬНІСТЬ"
                    </text>

                    <line x1="1030" y1={c2_cy} x2="1800" y2={c2_cy} stroke="#334155" stroke-width="1.5" stroke-dasharray="4 4" />
                    <line x1={c2_cx} y1="230" x2={c2_cx} y2="780" stroke="#334155" stroke-width="1.5" stroke-dasharray="4 4" />
                    <text x="1810" y={c2_cy + 5.0} font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"w1"</text>
                    <text x={c2_cx + 10.0} y="245" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"w2"</text>

                    <ellipse cx={c2_cx} cy={c2_cy} rx="340" ry="240" fill="none" stroke="#1e293b" stroke-width="1.5" />
                    <text x={c2_cx + 345.0} y={c2_cy - 8.0} font-family={FONT} font-size="11" fill={TEXT_DIM}>"L = 3.6"</text>

                    <ellipse cx={c2_cx} cy={c2_cy} rx="260" ry="180" fill="none" stroke="#1e293b" stroke-width="1.5" />
                    <text x={c2_cx + 265.0} y={c2_cy - 8.0} font-family={FONT} font-size="11" fill={TEXT_DIM}>"L = 2.0"</text>

                    <ellipse cx={c2_cx} cy={c2_cy} rx="180" ry="125" fill="none" stroke="#334155" stroke-width="1.5" />
                    <text x={c2_cx + 185.0} y={c2_cy - 8.0} font-family={FONT} font-size="11" fill={TEXT_MUTED}>"L = 0.9"</text>

                    <ellipse cx={c2_cx} cy={c2_cy} rx="110" ry="75" fill="none" stroke="#334155" stroke-width="1.5" />
                    <text x={c2_cx + 115.0} y={c2_cy - 8.0} font-family={FONT} font-size="11" fill={TEXT_MUTED}>"L = 0.3"</text>

                    <ellipse cx={c2_cx} cy={c2_cy} rx="50" ry="35" fill="none" stroke="#0284c7" stroke-width="1.5" stroke-dasharray="3 3" />

                    <line
                        x1={c2_cx + 2.40 * 115.0}
                        y1={c2_cy - 2.40 * 0.75 * 105.0}
                        x2={pt2_x}
                        y2={pt2_y}
                        stroke={COLOR_EMERALD}
                        stroke-width="3"
                        stroke-dasharray="4 4"
                        opacity="0.4"
                    />

                    <circle cx={c2_cx} cy={c2_cy} r="6" fill={COLOR_EMERALD} />
                    <circle cx={c2_cx} cy={c2_cy} r="24" fill={COLOR_EMERALD} opacity={format!("{:.2}", min_glow_opacity)} />
                    <text x={c2_cx} y={c2_cy + 22.0} font-family={FONT} font-size="12" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                        "Оптимум [0, 0]"
                    </text>

                    {
                        if grad2_mag > 0.05 {
                            fframes::svgr!(
                                <g>
                                    <line
                                        x1={c_tan1_x}
                                        y1={c_tan1_y}
                                        x2={c_tan2_x}
                                        y2={c_tan2_y}
                                        stroke="#64748b"
                                        stroke-width="2"
                                        stroke-dasharray="4 4"
                                    />
                                    <path
                                        d={format!("M {:.1} {:.1} L {:.1} {:.1} L {:.1} {:.1}", ra_p1_x, ra_p1_y, ra_p2_x, ra_p2_y, ra_p3_x, ra_p3_y)}
                                        fill="none"
                                        stroke={COLOR_CYAN}
                                        stroke-width="1.5"
                                    />
                                    <text
                                        x={ra_p2_x + 8.0}
                                        y={ra_p2_y - 8.0}
                                        font-family={FONT}
                                        font-size="11"
                                        font-weight="700"
                                        fill={COLOR_CYAN}
                                    >
                                        "90°"
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    {
                        if grad2_arrow_len > 12.0 {
                            fframes::svgr!(
                                <g>
                                    <line
                                        x1={pt2_x}
                                        y1={pt2_y}
                                        x2={pt2_grad_tip_x}
                                        y2={pt2_grad_tip_y}
                                        stroke={COLOR_ROSE}
                                        stroke-width="4.0"
                                        stroke-linecap="round"
                                        marker-end="url(#arrow-rose)"
                                    />
                                    <text
                                        x={pt2_grad_tip_x + 10.0}
                                        y={pt2_grad_tip_y - 6.0}
                                        font-family={FONT}
                                        font-size="13"
                                        font-weight="700"
                                        fill={COLOR_ROSE}
                                    >
                                        "grad L (Вгору)"
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    {
                        if desc2_arrow_len > 12.0 {
                            fframes::svgr!(
                                <g>
                                    <line
                                        x1={pt2_x}
                                        y1={pt2_y}
                                        x2={pt2_desc_tip_x}
                                        y2={pt2_desc_tip_y}
                                        stroke={COLOR_EMERALD}
                                        stroke-width="4.5"
                                        stroke-linecap="round"
                                        marker-end="url(#arrow-emerald)"
                                    />
                                    <text
                                        x={pt2_desc_tip_x - 10.0}
                                        y={pt2_desc_tip_y + 16.0}
                                        font-family={FONT}
                                        font-size="13"
                                        font-weight="700"
                                        fill={COLOR_EMERALD}
                                        text-anchor="end"
                                    >
                                        "-η·(grad L) (Спуск до центру)"
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    <circle cx={pt2_x} cy={pt2_y} r="22" fill="url(#glow-emerald)" opacity="0.6" />
                    <circle cx={pt2_x} cy={pt2_y} r="10" fill={TEXT_MAIN} stroke={COLOR_CYAN} stroke-width="3" />

                    <rect x={pt2_x - 85.0} y={pt2_y - 48.0} width="170" height="26" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1" />
                    <text x={pt2_x} y={pt2_y - 31.0} font-family={FONT} font-size="12" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        {format!("w = [{:.2}, {:.2}]", w1_val, w2_val)}
                    </text>

                    <g transform="translate(1005, 775)">
                        <circle cx="15" cy="15" r="6" fill={COLOR_CYAN} />
                        <text x="30" y="19" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN}>
                            "Ортогональність (90°): Градієнт завжди перпендикулярний до ізоліній однакового рівня втрат"
                        </text>

                        <circle cx="15" cy="42" r="6" fill={COLOR_EMERALD} />
                        <text x="30" y="46" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD}>
                            "Багатовимірність: grad L = [dL/dw1, dL/dw2]^T направляє рух точно у центр ями"
                        </text>
                    </g>
                </g>

                <g opacity={intro_alpha * loop_reset}>
                    <rect x="70" y="865" width="1780" height="185" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />

                    <rect x="95" y="885" width="400" height="28" rx="8" fill="#1e293b" />
                    <text x="110" y="904" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_AMBER} letter-spacing="1.0">
                        {phase_badge}
                    </text>
                    <text x="515" y="904" font-family={FONT} font-size="14" fill={TEXT_MUTED}>
                        {phase_slope_text}
                    </text>

                    <g transform="translate(100, 935)">
                        <text x="0" y="16" font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} letter-spacing="0.5">"ПОТОЧНИЙ СТАН W"</text>
                        <text x="0" y="44" font-family={FONT} font-size="24" font-weight="700" fill={COLOR_CYAN}>
                            {format!("w = {:.2}", w_val)}
                        </text>
                        <text x="0" y="66" font-family={FONT} font-size="12" fill={TEXT_MUTED}>
                            {format!("Втрати L(w) = {:.3}", loss_val)}
                        </text>
                    </g>

                    <line x1="480" y1="935" x2="480" y2="1025" stroke="#1e293b" stroke-width="1.5" />

                    <g transform="translate(520, 935)">
                        <text x="0" y="16" font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} letter-spacing="0.5">"ГРАДІЄНТ (НАХИЛ)"</text>
                        <text x="0" y="44" font-family={FONT} font-size="24" font-weight="700" fill={COLOR_ROSE}>
                            {format!("grad L = +{:.2}", grad_1d)}
                        </text>
                        <text x="0" y="66" font-family={FONT} font-size="12" fill={TEXT_MUTED}>
                            "Напрямок: Найкрутіший підйом вгору"
                        </text>
                    </g>

                    <line x1="930" y1="935" x2="930" y2="1025" stroke="#1e293b" stroke-width="1.5" />

                    <g transform="translate(970, 935)">
                        <text x="0" y="16" font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} letter-spacing="0.5">"КРУТИЗНА ТА ШВИДКІСТЬ"</text>
                        <text x="0" y="44" font-family={FONT} font-size="22" font-weight="700" fill={COLOR_AMBER}>
                            {
                                if grad_1d.abs() > 1.8 {
                                    "Крутий схил (|grad L| високий)"
                                } else if grad_1d.abs() > 0.2 {
                                    "Пологий схил (|grad L| малий)"
                                } else {
                                    "Дно яру: |grad L| ≈ 0 (Зупинка)"
                                }
                            }
                        </text>
                        <text x="0" y="66" font-family={FONT} font-size="12" fill={TEXT_MUTED}>
                            "Величина градієнта автоматично регулює крок"
                        </text>
                    </g>

                    <line x1="1400" y1="935" x2="1400" y2="1025" stroke="#1e293b" stroke-width="1.5" />

                    <g transform="translate(1440, 935)">
                        <text x="0" y="16" font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} letter-spacing="0.5">"КРОК ОНОВЛЕННЯ ВАГ (SGD)"</text>
                        <text x="0" y="44" font-family={FONT} font-size="20" font-weight="700" fill={COLOR_EMERALD}>
                            "w_новий = w - η·(grad L)"
                        </text>
                        <text x="0" y="66" font-family={FONT} font-size="13" font-weight="600" fill={TEXT_MAIN}>
                            {phase_lr_text}
                        </text>
                    </g>
                </g>
            </svg>
        )
    }
}
