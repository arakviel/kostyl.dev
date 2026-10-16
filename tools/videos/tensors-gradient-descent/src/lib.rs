//! Gradient descent for f(x) = (x-3)^2, x0=-2, lr=0.1.
//! Ball rolls along parabola to x*=3. 10s loop, dark theme.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct GdMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

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

pub struct GdVideo<'a> {
    pub media: &'a GdMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> GdVideo<'a> {
    pub fn new(media: &'a GdMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for GdVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GdVideo").finish()
    }
}

impl fframes::Video for GdVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.0)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(3.0)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(5.0)..AudioTimestamp::Eof)
                .gain_db(-1.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(7.6)..AudioTimestamp::Eof)
                .gain_db(1.0),
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
        let g_alpha = intro_alpha * loop_reset;

        // GD trajectory matching lr=0.1: x(t) = 3 - 5*exp(-0.55*teff), teff in [0,8]
        let teff = clamp(t, 0.0, 8.6);
        let x_val = 3.0 - 5.0 * (-0.55 * teff).exp();
        let loss_val = (x_val - 3.0) * (x_val - 3.0);
        let grad_val = 2.0 * (x_val - 3.0);
        let iter = (teff * 5.8) as i32; // ~50 iters by t=8.6

        // Parabola screen mapping: x in [-3, 5], loss in [0, 30]
        // Plot area: px 150..1230, baseline y=700, top y=220
        let px_lo = 150.0;
        let px_hi = 1230.0;
        let x_lo = -2.2;
        let x_hi = 5.0;
        let map_x = |x: f32| px_lo + (x - x_lo) / (x_hi - x_lo) * (px_hi - px_lo);
        let base_y = 700.0;
        let loss_h = |l: f32| clamp(l, 0.0, 30.0) / 30.0 * 440.0;
        let map_y = |l: f32| base_y - loss_h(l);

        let ball_x = map_x(x_val);
        let ball_y = map_y(loss_val);

        // Trail: sample teff history
        let mut trail = String::new();
        let n = 40;
        for i in 0..n {
            let tt = teff * i as f32 / n as f32;
            let xx = 3.0 - 5.0 * (-0.55 * tt).exp();
            let ll = (xx - 3.0) * (xx - 3.0);
            let px = px_lo + (xx - x_lo) / (x_hi - x_lo) * (px_hi - px_lo);
            let py = base_y - clamp(ll, 0.0, 30.0) / 30.0 * 440.0;
            if i == 0 {
                trail.push_str(&format!("M {px:.1} {py:.1}"));
            } else {
                trail.push_str(&format!(" L {px:.1} {py:.1}"));
            }
        }

        // Full parabola f(x) = (x-3)^2 for x in [-3, 5] (static curve, computed)
        let mut parabola = String::new();
        let steps = 80;
        for i in 0..=steps {
            let xx = x_lo + (x_hi - x_lo) * i as f32 / steps as f32;
            let ll = (xx - 3.0) * (xx - 3.0);
            let px = px_lo + (xx - x_lo) / (x_hi - x_lo) * (px_hi - px_lo);
            let py = base_y - clamp(ll, 0.0, 30.0) / 30.0 * 440.0;
            if i == 0 {
                parabola.push_str(&format!("M {px:.1} {py:.1}"));
            } else {
                parabola.push_str(&format!(" L {px:.1} {py:.1}"));
            }
        }

        // Tangent slope angle for grad arrow
        let slope = 2.0 * (x_val - 3.0); // df/dx
        let grad_len = clamp(slope.abs() * 14.0, 0.0, 150.0);
        // arrow points uphill (+grad), descent step opposite
        let dir = if slope >= 0.0 { 1.0 } else { -1.0 };
        let tip_up_x = ball_x + dir * grad_len;
        let tip_up_y = ball_y - dir * slope.abs() * 4.0 - 10.0;
        let tip_dn_x = ball_x - dir * grad_len * 0.8;
        let tip_dn_y = ball_y + dir * slope.abs() * 3.0 + 8.0;

        let converged = if (x_val - 3.0).abs() < 0.08 { 1.0 } else { 0.0 };
        let glow = if t > 7.0 {
            0.4 + 0.4 * ((t - 7.0) * 4.0).sin().abs()
        } else {
            0.0
        };

        // Optimum screen pos
        let opt_x = map_x(3.0);
        let opt_y = map_y(0.0);

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <radialGradient id="bg-glow" cx="0.5" cy="0.4" r="0.65">
                        <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.35" />
                        <stop offset="60%" stop-color="#0b1329" stop-opacity="0.10" />
                        <stop offset="100%" stop-color={BG_COLOR} stop-opacity="0" />
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
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH / 2} cy={HEIGHT / 2} r="800" fill="url(#bg-glow)" />

                <g opacity={g_alpha}>
                    <rect x="620" y="24" width="680" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "AUTOGRAD В ДІЇ: РУЧНИЙ ГРАДІЄНТНИЙ СПУСК КРОК ЗА КРОКОМ"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "f(x) = (x − 3)²: від x = −2 до мінімуму x* = 3"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "lr = 0.1, 50 ітерацій: loss.backward() → x -= lr · x.grad → zero_() → повтор"
                    </text>
                </g>

                // ---- Plot card ----
                <g opacity={g_alpha}>
                    <rect x="70" y="155" width="1240" height="640" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    // axes
                    <line x1={px_lo} y1={base_y} x2={px_hi} y2={base_y} stroke="#334155" stroke-width="2" />
                    <line x1={map_x(0.0)} y1="200" x2={map_x(0.0)} y2={base_y + 20.0} stroke="#334155" stroke-width="1.5" stroke-dasharray="5 4" />
                    <text x={px_hi + 8.0} y={base_y + 6.0} font-family={FONT} font-size="14" font-weight="700" fill={TEXT_DIM}>"x"</text>
                    <text x={map_x(0.0) + 8.0} y="215" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_DIM}>"f(x)"</text>
                    // x ticks
                    <text x={map_x(-2.0)} y={base_y + 26.0} font-family={FONT} font-size="13" fill={TEXT_MUTED} text-anchor="middle">"−2 (старт)"</text>
                    <text x={map_x(3.0)} y={base_y + 26.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"3 (мінімум)"</text>
                    // parabola curve f(x) = (x-3)^2 (computed, matches ball physics)
                    <path d={parabola} fill="none" stroke="#0284c7" stroke-width="3.5" />
                    // trail traveled
                    <path d={trail} fill="none" stroke={COLOR_EMERALD} stroke-width="4" stroke-dasharray="6 5" opacity="0.7" />
                    // optimum marker
                    <circle cx={opt_x} cy={opt_y} r="7" fill={COLOR_EMERALD} />
                    <circle cx={opt_x} cy={opt_y} r="22" fill={COLOR_EMERALD} opacity={format!("{:.2}", glow * loop_reset)} />
                    <text x={opt_x + 18.0} y={base_y - 12.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD}>"f(3) = 0"</text>
                    // start marker
                    <circle cx={map_x(-2.0)} cy={map_y(25.0)} r="7" fill={TEXT_DIM} />
                    <text x={map_x(-2.0)} y={map_y(25.0) - 14.0} font-family={FONT} font-size="13" fill={TEXT_MUTED} text-anchor="middle">"f(−2) = 25"</text>
                    // grad arrows (hide when converged)
                    <g opacity={1.0 - converged}>
                        <line x1={ball_x} y1={ball_y} x2={tip_up_x} y2={tip_up_y} stroke={COLOR_ROSE} stroke-width="4" stroke-linecap="round" marker-end="url(#arrow-rose)" />
                        <text x={tip_up_x + 10.0} y={tip_up_y - 4.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_ROSE}>" +grad (вгору)"</text>
                        <line x1={ball_x} y1={ball_y} x2={tip_dn_x} y2={tip_dn_y} stroke={COLOR_EMERALD} stroke-width="4.5" stroke-linecap="round" marker-end="url(#arrow-emerald)" />
                        <text x={tip_dn_x - 10.0} y={tip_dn_y + 18.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD} text-anchor="end">"−lr·grad (крок)"</text>
                    </g>
                    // ball
                    <circle cx={ball_x} cy={ball_y} r="24" fill={COLOR_EMERALD} opacity="0.25" />
                    <circle cx={ball_x} cy={ball_y} r="11" fill={TEXT_MAIN} stroke={COLOR_CYAN} stroke-width="3" />
                    <rect x={ball_x - 80.0} y={ball_y - 92.0} width="160" height="28" rx="7" fill="#0f172a" stroke="#334155" stroke-width="1" />
                    <text x={ball_x} y={ball_y - 73.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        {format!("x = {:.2}", x_val)}
                    </text>
                </g>

                // ---- Stats card ----
                <g opacity={g_alpha}>
                    <rect x="1340" y="155" width="510" height="640" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="1365" y="175" width="280" height="30" rx="8" fill="#1e293b" />
                    <text x="1380" y="195" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_AMBER} letter-spacing="1.0">
                        "СТАН ОПТИМІЗАЦІЇ"
                    </text>
                    <g transform="translate(1370, 250)">
                        <text x="0" y="0" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"ІТЕРАЦІЯ"</text>
                        <text x="0" y="40" font-family={FONT} font-size="34" font-weight="700" fill={COLOR_CYAN}>{format!("{iter} / 50")}</text>
                        <text x="0" y="70" font-family={FONT} font-size="13" fill={TEXT_MUTED}>"кожен крок: forward → backward → update"</text>
                    </g>
                    <line x1="1370" y1="350" x2="1820" y2="350" stroke="#1e293b" stroke-width="1.5" />
                    <g transform="translate(1370, 380)">
                        <text x="0" y="0" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"ВТРАТИ f(x) = (x−3)²"</text>
                        <text x="0" y="40" font-family={FONT} font-size="34" font-weight="700" fill={COLOR_EMERALD}>{format!("{:.4}", loss_val)}</text>
                        <text x="0" y="70" font-family={FONT} font-size="13" fill={TEXT_MUTED}>"старт 25.0 → ціль 0.0"</text>
                    </g>
                    <line x1="1370" y1="480" x2="1820" y2="480" stroke="#1e293b" stroke-width="1.5" />
                    <g transform="translate(1370, 510)">
                        <text x="0" y="0" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_DIM}>"ГРАДІЄНТ df/dx = 2(x−3)"</text>
                        <text x="0" y="40" font-family={FONT} font-size="34" font-weight="700" fill={COLOR_ROSE}>{format!("{:.2}", grad_val)}</text>
                        <text x="0" y="70" font-family={FONT} font-size="13" fill={TEXT_MUTED}>"крок: x -= 0.1 · grad"</text>
                    </g>
                    <g transform="translate(1370, 640)">
                        <rect x="0" y="0" width="450" height="120" rx="12" fill={if converged > 0.5 { "#064e3b" } else { "#1e293b" }} stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x="225" y="34" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                            {if converged > 0.5 { "ЗБІЖНІСТЬ ДОСЯГНУТО" } else { "СПУСК ТРИВАЄ..." }}
                        </text>
                        <text x="225" y="60" font-family={FONT} font-size="13" fill={TEXT_MAIN} text-anchor="middle">"x → 3.0 (оптимум)"</text>
                        <text x="225" y="84" font-family={FONT} font-size="13" fill={TEXT_MUTED} text-anchor="middle">"оновлення під torch.no_grad()"</text>
                    </g>
                </g>

                // ---- Bottom code bar ----
                <g opacity={g_alpha}>
                    <rect x="70" y="815" width="1780" height="195" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g transform="translate(110, 860)">
                        <text x="0" y="0" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">"ЦИКЛ ЗІ СТАТТІ (GRADIENT_DESCENT_MANUAL.IPYNB)"</text>
                        <text x="0" y="34" font-family={FONT} font-size="17" fill={TEXT_MAIN}>"loss = (x − 3)**2;  loss.backward();  x -= 0.1 * x.grad;  x.grad.zero_()"</text>
                        <text x="0" y="64" font-family={FONT} font-size="14" fill={TEXT_MUTED}>"ітерації 0/10/20/30/40: x = −1.00 / 2.57 / 2.95 / 2.995 / 2.9995 → 2.9999"</text>
                        <text x="0" y="94" font-family={FONT} font-size="14" fill={TEXT_DIM}>"без zero_() градієнти накопичуються: x.grad = 6.0 → 12.0 (пастка!)"</text>
                    </g>
                    <g transform="translate(1420, 845)">
                        <rect x="0" y="0" width="400" height="135" rx="12" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x="200" y="34" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"ОНОВЛЕННЯ ПІД no_grad()"</text>
                        <text x="200" y="64" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"рух проти градієнта:"</text>
                        <text x="200" y="92" font-family={FONT} font-size="17" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"x := x - lr*grad"</text>
                    </g>
                </g>
            </svg>
        )
    }
}
