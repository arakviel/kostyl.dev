//! Gradient intuition on loss mountain: hiker in fog, +grad arrow uphill (red),
//! -grad arrow downhill (green), 3 steps to valley, sign rules. 10s loop, dark.

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct CgMedia, "media");

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

#[inline]
fn lerp(a: f32, b: f32, p: f32) -> f32 {
    a + (b - a) * p
}

pub struct CgVideo<'a> {
    pub media: &'a CgMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> CgVideo<'a> {
    pub fn new(media: &'a CgMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for CgVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CgVideo").finish()
    }
}

impl fframes::Video for CgVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.6)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.0)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(6.6)..AudioTimestamp::Eof)
                .gain_db(0.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(8.0)..AudioTimestamp::Eof)
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

        // Hiker journey: -1.0 -> 1.2 -> 2.5 -> 3.0 (valley)
        let x_val = if t < 1.5 {
            -1.0
        } else if t < 3.8 {
            lerp(-1.0, 1.2, ease_in_out((t - 1.5) / 2.3))
        } else if t < 6.2 {
            lerp(1.2, 2.5, ease_in_out((t - 3.8) / 2.4))
        } else if t < 8.0 {
            lerp(2.5, 3.0, ease_in_out((t - 6.2) / 1.8))
        } else {
            3.0
        };
        // Loss surface f(x) = (x-3)^2 scaled for mountain look
        let loss_val = (x_val - 3.0) * (x_val - 3.0);
        let grad_val = 2.0 * (x_val - 3.0);

        // Plot mapping: x in [-2.5, 5.5], loss in [0, 30]
        let px_lo = 120.0;
        let px_hi = 1300.0;
        let x_lo = -2.5;
        let x_hi = 5.5;
        let base_y = 720.0;
        let map_x = |x: f32| px_lo + (x - x_lo) / (x_hi - x_lo) * (px_hi - px_lo);
        let map_y = |l: f32| base_y - clamp(l, 0.0, 30.0) / 30.0 * 460.0;
        let ball_x = map_x(x_val);
        let ball_y = map_y(loss_val);

        // Full surface path
        let mut surface = String::new();
        let steps = 90;
        for i in 0..=steps {
            let xx = x_lo + (x_hi - x_lo) * i as f32 / steps as f32;
            let ll = (xx - 3.0) * (xx - 3.0);
            let px = px_lo + (xx - x_lo) / (x_hi - x_lo) * (px_hi - px_lo);
            let py = base_y - clamp(ll, 0.0, 30.0) / 30.0 * 460.0;
            if i == 0 {
                surface.push_str(&format!("M {px:.1} {py:.1}"));
            } else {
                surface.push_str(&format!(" L {px:.1} {py:.1}"));
            }
        }

        // Fog drift
        let fog_x = ((t * 30.0) % 200.0) - 100.0;

        // Arrow sizes from |grad|
        let alen = clamp(grad_val.abs() * 13.0, 0.0, 150.0);
        let dir = if grad_val >= 0.0 { -1.0 } else { 1.0 };
        // uphill tip (gradient, red): opposite of descent
        let up_x = ball_x + dir * alen;
        let up_y = ball_y - alen * 0.55 - 8.0;
        // downhill tip (antigradient, green)
        let dn_x = ball_x - dir * alen * 0.9;
        let dn_y = ball_y + alen * 0.45 + 8.0;
        let arrows_on = if grad_val.abs() > 0.25 { 1.0 } else { 0.0 };

        let opt_x = map_x(3.0);
        let opt_y = map_y(0.0);
        let glow = if t > 7.6 {
            0.4 + 0.4 * ((t - 7.6) * 4.0).sin().abs()
        } else {
            0.0
        };

        // Phase badge + advice
        let (badge, advice, rule) = if grad_val > 0.25 {
            (
                "ГРАДІЄНТ > 0: ПІДЙОМ ПРАВОРУЧ",
                "збільшення w збільшує Loss → ЗМЕНШУЙ w",
                "крок: w := w - lr·grad (ліворуч, вниз)",
            )
        } else if grad_val < -0.25 {
            (
                "ГРАДІЄНТ < 0: ПІДЙОМ ЛІВОРУЧ",
                "збільшення w зменшує Loss → ЗБІЛЬШУЙ w",
                "крок: w := w - lr·grad (праворуч, вниз)",
            )
        } else {
            (
                "ГРАДІЄНТ = 0: ДНО ДОЛИНИ",
                "оптимум досягнуто → ЗУПИНИСЬ",
                "grad = 0 → крок нульовий, w* = 3",
            )
        };

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
                    <linearGradient id="fog" x1="0" y1="0" x2="1" y2="0">
                        <stop offset="0%" stop-color="#94a3b8" stop-opacity="0" />
                        <stop offset="50%" stop-color="#94a3b8" stop-opacity="0.14" />
                        <stop offset="100%" stop-color="#94a3b8" stop-opacity="0" />
                    </linearGradient>
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH / 2} cy={HEIGHT / 2} r="800" fill="url(#bg-glow)" />

                <g opacity={g_alpha}>
                    <rect x="580" y="24" width="760" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "ІНТУЇЦІЯ ГРАДІЄНТА: ТУРИСТ У ТУМАНІ НА СХИЛІ ВТРАТ"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Висота = помилка: вершина — хаос, долина — точність"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={COLOR_AMBER} text-anchor="middle">
                        {badge}
                    </text>
                </g>

                // ---- Mountain card ----
                <g opacity={g_alpha}>
                    <rect x="70" y="155" width="1300" height="640" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    // surface
                    <path d={surface} fill="none" stroke="#0284c7" stroke-width="3.5" />
                    // fog bands drifting
                    <rect x={200.0 + fog_x} y="260" width="900" height="70" rx="35" fill="url(#fog)" />
                    <rect x={500.0 - fog_x} y="420" width="700" height="60" rx="30" fill="url(#fog)" opacity="0.7" />
                    // peak + valley labels
                    <text x={map_x(-2.0)} y={map_y(25.0) - 24.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_ROSE} text-anchor="middle">"ВЕРШИНА: велика помилка"</text>
                    <circle cx={map_x(-2.0)} cy={map_y(25.0)} r="6" fill={COLOR_ROSE} />
                    <text x={opt_x + 90.0} y={base_y - 18.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_EMERALD}>"ДНО: Loss = 0"</text>
                    <circle cx={opt_x} cy={opt_y} r="7" fill={COLOR_EMERALD} />
                    <circle cx={opt_x} cy={opt_y} r="24" fill={COLOR_EMERALD} opacity={format!("{:.2}", glow * loop_reset)} />
                    // axes
                    <line x1={px_lo} y1={base_y} x2={px_hi} y2={base_y} stroke="#334155" stroke-width="2" />
                    <text x={map_x(-2.2)} y={base_y + 28.0} font-family={FONT} font-size="13" fill={TEXT_MUTED}>"w (вага)"</text>
                    <text x={px_hi - 90.0} y={base_y - 420.0} font-family={FONT} font-size="13" fill={TEXT_MUTED}>"Loss"</text>
                    // hiker
                    <circle cx={ball_x} cy={ball_y} r="26" fill={COLOR_CYAN} opacity="0.25" />
                    <circle cx={ball_x} cy={ball_y} r="12" fill={TEXT_MAIN} stroke={COLOR_CYAN} stroke-width="3" />
                    <text x={ball_x} y={ball_y - 34.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"турист (w)"</text>
                    // arrows
                    <g opacity={arrows_on}>
                        <line x1={ball_x} y1={ball_y} x2={up_x} y2={up_y} stroke={COLOR_ROSE} stroke-width="4" stroke-linecap="round" marker-end="url(#arrow-rose)" />
                        <text x={up_x + 12.0} y={up_y - 2.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_ROSE}>"+grad: найкрутіший підйом"</text>
                        <line x1={ball_x} y1={ball_y} x2={dn_x} y2={dn_y} stroke={COLOR_EMERALD} stroke-width="4.5" stroke-linecap="round" marker-end="url(#arrow-emerald)" />
                        <text x={dn_x - 12.0} y={dn_y + 22.0} font-family={FONT} font-size="14" font-weight="700" fill={COLOR_EMERALD} text-anchor="end">"-grad: найшвидший спуск"</text>
                    </g>
                    // readout (fixed panel, top-right inside card)
                    <rect x="1000" y="180" width="330" height="70" rx="10" fill="#0f172a" stroke="#334155" stroke-width="1.5" />
                    <text x="1165" y="208" font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        {format!("w = {:.2}  grad = {:+.2}", x_val, grad_val)}
                    </text>
                    <text x="1165" y="232" font-family={FONT} font-size="13" fill={TEXT_MUTED} text-anchor="middle">{advice}</text>
                </g>

                // ---- Rules card ----
                <g opacity={g_alpha}>
                    <rect x="1400" y="155" width="450" height="640" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="1425" y="175" width="300" height="30" rx="8" fill="#1e293b" />
                    <text x="1440" y="195" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_AMBER} letter-spacing="1.0">
                        "ЯК ЧИТАТИ ЗНАК"
                    </text>
                    <g transform="translate(1430, 260)">
                        <rect x="0" y="0" width="390" height="110" rx="12" fill="#4c0519" stroke={COLOR_ROSE} stroke-width="1.5" />
                        <text x="195" y="32" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_ROSE} text-anchor="middle">"grad > 0"</text>
                        <text x="195" y="58" font-family={FONT} font-size="13" fill={TEXT_MAIN} text-anchor="middle">"ріст w ростить Loss"</text>
                        <text x="195" y="82" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"→ зменшуй w"</text>
                    </g>
                    <g transform="translate(1430, 390)">
                        <rect x="0" y="0" width="390" height="110" rx="12" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x="195" y="32" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"grad < 0"</text>
                        <text x="195" y="58" font-family={FONT} font-size="13" fill={TEXT_MAIN} text-anchor="middle">"ріст w ріже Loss"</text>
                        <text x="195" y="82" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"→ збільшуй w"</text>
                    </g>
                    <g transform="translate(1430, 520)">
                        <rect x="0" y="0" width="390" height="110" rx="12" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x="195" y="32" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"grad = 0"</text>
                        <text x="195" y="58" font-family={FONT} font-size="13" fill={TEXT_MAIN} text-anchor="middle">"дно досягнуто"</text>
                        <text x="195" y="82" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"→ оптимум w*"</text>
                    </g>
                    <text x="1625" y="670" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="middle">"мінус розвертає стрілку вниз"</text>
                </g>

                // ---- Bottom formula ----
                <g opacity={g_alpha}>
                    <rect x="70" y="820" width="1780" height="190" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g transform="translate(110, 862)">
                        <text x="0" y="0" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">"ОНОВЛЕННЯ ВАГИ: КРОК ПРОТИ ГРАДІЄНТА"</text>
                        <text x="0" y="44" font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN}>"w_новий  =  w − lr · grad Loss"</text>
                        <text x="620" y="44" font-family={FONT} font-size="15" fill={TEXT_MUTED}>{rule}</text>
                        <text x="0" y="82" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"lr (learning rate) — довжина кроку: завеликий стрибає через долину, замалий повзе"</text>
                    </g>
                    <g transform="translate(1430, 850)">
                        <rect x="0" y="0" width="390" height="130" rx="12" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x="195" y="36" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"АНТИГРАДІЄНТ"</text>
                        <text x="195" y="66" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"мінус перед градієнтом"</text>
                        <text x="195" y="94" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"вказує точно вниз"</text>
                    </g>
                </g>
            </svg>
        )
    }
}
