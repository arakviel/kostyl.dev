//! CPU vs GPU matmul benchmark: 5000x5000, CPU 1.4280s vs GPU 0.0245s = 58.3x.
//! Plus data flow RAM -> PCIe -> VRAM. 10s loop, dark theme.

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
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(2.0)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(3.0)..AudioTimestamp::Eof)
                .gain_db(0.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(5.6)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(6.4)..AudioTimestamp::Eof)
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

        // Race progress 2.0 -> 5.5
        let rp = ease_in_out(clamp((t - 2.0) / 3.5, 0.0, 1.0));
        let cpu_fill = rp;
        let cpu_time = 1.4280 * rp;
        // GPU finishes in first 15% of the race window
        let gp = clamp(rp / 0.15, 0.0, 1.0);
        let gpu_fill = gp;
        let gpu_time = 0.0245 * gp;
        let speedup = if gpu_time > 0.0005 {
            (cpu_time / gpu_time).min(58.3)
        } else {
            0.0
        };
        let badge_op = clamp((t - 5.6) / 0.8, 0.0, 1.0);
        let badge_glow = if t > 6.2 {
            0.4 + 0.4 * ((t - 6.2) * 3.0).sin().abs()
        } else {
            0.0
        };

        // Flow dot RAM -> VRAM -> RAM (loop over whole video)
        let cyc = (t % 6.0) / 6.0;
        let (dot_x, dot_label) = if cyc < 0.4 {
            let p = ease_in_out(cyc / 0.4);
            (lerp(330.0, 1300.0, p), ".to('cuda')")
        } else if cyc < 0.55 {
            (1300.0, "обчислення на GPU")
        } else if cyc < 0.95 {
            let p = ease_in_out((cyc - 0.55) / 0.4);
            (lerp(1300.0, 330.0, p), ".to('cpu')")
        } else {
            (330.0, ".numpy()")
        };

        let bar_w = 740.0;

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
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH / 2} cy={HEIGHT / 2} r="800" fill="url(#bg-glow)" />

                <g opacity={g_alpha}>
                    <rect x="600" y="24" width="720" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "ЗАЛІЗО: ЧОМУ NEURAL NETWORKS ТРЕНУЮТЬ НА GPU"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Множення матриць 5000×5000: CPU vs GPU"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "RTX 3080, Compute Capability 8.6, CUDA 12.1 — той самий код, інший пристрій"
                    </text>
                </g>

                // ---- CPU card ----
                <g opacity={g_alpha}>
                    <rect x="70" y="155" width="860" height="440" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="95" y="175" width="420" height="30" rx="8" fill="#1e293b" />
                    <text x="110" y="195" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_MUTED} letter-spacing="1.0">
                        "CPU: 4-16 ПОТУЖНИХ ЯДЕР, ПОСЛІДОВНІ ОБЧИСЛЕННЯ"
                    </text>
                    <text x="110" y="280" font-family={FONT} font-size="52" font-weight="700" fill={COLOR_ROSE}>
                        {format!("{:.4} c", cpu_time)}
                    </text>
                    <text x="110" y="315" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"x_cpu @ y_cpu  (device='cpu')"</text>
                    <rect x="110" y="350" width={bar_w} height="44" rx="12" fill="#1e293b" />
                    <rect x="110" y="350" width={bar_w * cpu_fill} height="44" rx="12" fill={COLOR_ROSE} opacity="0.85" />
                    <text x="110" y="440" font-family={FONT} font-size="14" fill={TEXT_DIM}>"велика кеш-пам'ять L1/L2/L3, низька затримка — але мало паралелізму"</text>
                    <text x="110" y="540" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"ядра: десятки  |  матриці: повільно"</text>
                </g>

                // ---- VS badge ----
                <g opacity={g_alpha}>
                    <circle cx="960" cy="375" r="44" fill="#0f172a" stroke={COLOR_AMBER} stroke-width="2.5" />
                    <text x="960" y="388" font-family={FONT} font-size="26" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">"VS"</text>
                </g>

                // ---- GPU card ----
                <g opacity={g_alpha}>
                    <rect x="990" y="155" width="860" height="440" rx="18" fill={CARD_BG} stroke={COLOR_EMERALD} stroke-width="1.5" stroke-opacity="0.6" />
                    <rect x="1015" y="175" width="480" height="30" rx="8" fill="#1e293b" />
                    <text x="1030" y="195" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD} letter-spacing="1.0">
                        "GPU: ТИСЯЧІ CUDA + TENSOR CORES, SIMD-ПАРАЛЕЛІЗМ"
                    </text>
                    <text x="1030" y="280" font-family={FONT} font-size="52" font-weight="700" fill={COLOR_EMERALD}>
                        {format!("{:.4} c", gpu_time)}
                    </text>
                    <text x="1030" y="315" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"x_gpu @ y_gpu  (device='cuda') + synchronize()"</text>
                    <rect x="1030" y="350" width={bar_w} height="44" rx="12" fill="#1e293b" />
                    <rect x="1030" y="350" width={bar_w * gpu_fill} height="44" rx="12" fill={COLOR_EMERALD} opacity="0.9" />
                    <text x="1030" y="440" font-family={FONT} font-size="14" fill={TEXT_DIM}>"HBM/GDDR6, Tensor Cores 4-го покоління — у 20-100 разів швидше"</text>
                    <text x="1030" y="540" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"ядра: тисячі  |  матриці: миттєво"</text>
                </g>

                // ---- Speedup badge ----
                <g opacity={badge_op * g_alpha}>
                    <rect x="660" y="470" width="600" height="90" rx="16" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                    <circle cx="660" cy="515" r="30" fill={COLOR_EMERALD} opacity={format!("{:.2}", badge_glow)} />
                    <text x="960" y="510" font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        {format!("Прискорення: {:.1}x", speedup)}
                    </text>
                    <text x="960" y="540" font-family={FONT} font-size="14" fill={COLOR_EMERALD} text-anchor="middle">"1.4280 c / 0.0245 c — той самий оператор @ "</text>
                </g>

                // ---- Flow bar: RAM -> PCIe -> VRAM ----
                <g opacity={g_alpha}>
                    <rect x="70" y="620" width="1780" height="390" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="95" y="640" width="420" height="28" rx="8" fill="#1e293b" />
                    <text x="110" y="659" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">
                        "ПОТІК ДАНИХ: ХОСТ-ПАМ'ЯТЬ → ШИНА → ВІДЕОПАМ'ЯТЬ"
                    </text>
                    // nodes
                    <g>
                        <rect x="130" y="720" width="400" height="120" rx="14" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="2" />
                        <text x="330" y="760" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"Хост (CPU RAM)"</text>
                        <text x="330" y="788" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"t_cpu, датасет, батчі"</text>
                        <text x="330" y="812" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="middle">"завантаження з SSD"</text>
                    </g>
                    <g>
                        <rect x="580" y="720" width="400" height="120" rx="14" fill="#1e293b" stroke={COLOR_AMBER} stroke-width="2" />
                        <text x="780" y="760" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">"PCIe 4.0 / NVLink"</text>
                        <text x="780" y="788" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"шина передачі"</text>
                        <text x="780" y="812" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="middle">"вузьке місце пайплайна"</text>
                    </g>
                    <g>
                        <rect x="1030" y="720" width="540" height="120" rx="14" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x="1300" y="760" font-family={FONT} font-size="18" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"Пристрій (GPU VRAM)"</text>
                        <text x="1300" y="788" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"t_gpu, cuBLAS / cuDNN ядра"</text>
                        <text x="1300" y="812" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="middle">"torch.cuda.synchronize() для замірiв"</text>
                    </g>
                    // lane + moving dot
                    <line x1="150" y1="890" x2="1550" y2="890" stroke="#334155" stroke-width="3" />
                    <circle cx={dot_x} cy="890" r="12" fill={COLOR_AMBER} />
                    <circle cx={dot_x} cy="890" r="22" fill={COLOR_AMBER} opacity="0.3" />
                    <rect x={dot_x - 90.0} y="912" width="180" height="30" rx="8" fill="#0f172a" stroke={COLOR_AMBER} stroke-width="1.5" />
                    <text x={dot_x} y="932" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">{dot_label}</text>
                    <text x="960" y="975" font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">
                        "агностічний патерн: device = 'cuda' if available else 'cpu'  |  несумісні пристрої → RuntimeError"
                    </text>
                </g>
            </svg>
        )
    }
}
