//! Tensor rank hierarchy: 0D scalar -> 1D vector -> 2D matrix -> 3D RGB -> 4D batch.
//! Cards light up in sequence, axis count grows. 10s loop, dark theme.

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
const COLOR_INDIGO: &str = "#818cf8";
const COLOR_EMERALD: &str = "#10b981";
const COLOR_AMBER: &str = "#f59e0b";
const COLOR_ROSE: &str = "#f43f5e";

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
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.4)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(3.0)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.6)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(6.2)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(7.6)..AudioTimestamp::Eof)
                .gain_db(0.0),
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

        // Staggered activation: card i lights at 1.0 + i*1.3
        let act = |i: f32| ease_out_cubic(clamp((t - (1.0 + i * 1.3)) / 0.7, 0.0, 1.0));
        let a0 = act(0.0);
        let a1 = act(1.0);
        let a2 = act(2.0);
        let a3 = act(3.0);
        let a4 = act(4.0);

        // Axis counter: lit cards minus one (0D has ndim 0)
        let lit = a0 + a1 + a2 + a3 + a4;
        let (cur_shape, cur_ex) = if lit < 0.5 {
            ("—", "—")
        } else {
            match ((lit - 1.0).round() as i32).clamp(0, 4) {
                0 => ("[]", "скаляр: температура"),
                1 => ("[3]", "вектор: ціни"),
                2 => ("[3, 3]", "матриця: таблиця"),
                3 => ("[3, H, W]", "RGB зображення"),
                _ => ("[B, C, H, W]", "батч зображень"),
            }
        };
        let ndim = if lit < 0.5 {
            0
        } else {
            ((lit - 1.0).round() as i32).clamp(0, 4)
        };

        // Card geometry: 5 cards
        let cw = 336.0;
        let gap = 16.0;
        let x0 = 70.0;
        let cy = 200.0;
        let ch = 600.0;
        let cx = |i: f32| x0 + i * (cw + gap);

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
                    <rect x="660" y="24" width="600" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "АНАТОМІЯ ТЕНЗОРА: РАНГ = КІЛЬКІСТЬ ОСЕЙ"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Від скаляра до батчу: кожна вісь додає вимір"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "torch.tensor(42) → tensor([1,2,3]) → zeros(3,3) → RGB [3,H,W] → батч [B,C,H,W]"
                    </text>
                </g>

                // ---- Card 0D ----
                <g opacity={g_alpha}>
                    <rect x={cx(0.0)} y={cy} width={cw} height={ch} rx="18" fill={CARD_BG} stroke={if a0 > 0.5 { COLOR_CYAN } else { CARD_BORDER }} stroke-width={if a0 > 0.5 { 2.5 } else { 1.5 }} />
                    <rect x={cx(0.0) + 20.0} y={cy + 20.0} width="180" height="30" rx="8" fill="#1e293b" />
                    <text x={cx(0.0) + 32.0} y={cy + 40.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN}>"0D: СКАЛЯР"</text>
                    <g opacity={a0}>
                        <circle cx={cx(0.0) + cw / 2.0} cy={cy + 220.0} r="52" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="3" />
                        <text x={cx(0.0) + cw / 2.0} y={cy + 232.0} font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"42"</text>
                        <text x={cx(0.0) + cw / 2.0} y={cy + 340.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"shape = []"</text>
                        <text x={cx(0.0) + cw / 2.0} y={cy + 372.0} font-family={FONT} font-size="15" fill={TEXT_MUTED} text-anchor="middle">"ndim = 0"</text>
                        <text x={cx(0.0) + cw / 2.0} y={cy + 440.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"одне число:"</text>
                        <text x={cx(0.0) + cw / 2.0} y={cy + 464.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"температура, вік"</text>
                        <text x={cx(0.0) + cw / 2.0} y={cy + 520.0} font-family={FONT} font-size="13" fill={COLOR_CYAN} text-anchor="middle">"tensor(42).item() → 42"</text>
                    </g>
                </g>

                // ---- Card 1D ----
                <g opacity={g_alpha}>
                    <rect x={cx(1.0)} y={cy} width={cw} height={ch} rx="18" fill={CARD_BG} stroke={if a1 > 0.5 { COLOR_CYAN } else { CARD_BORDER }} stroke-width={if a1 > 0.5 { 2.5 } else { 1.5 }} />
                    <rect x={cx(1.0) + 20.0} y={cy + 20.0} width="180" height="30" rx="8" fill="#1e293b" />
                    <text x={cx(1.0) + 32.0} y={cy + 40.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN}>"1D: ВЕКТОР"</text>
                    <g opacity={a1}>
                        <rect x={cx(1.0) + 38.0} y={cy + 170.0} width="80" height="70" rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="2" />
                        <text x={cx(1.0) + 78.0} y={cy + 214.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"1"</text>
                        <rect x={cx(1.0) + 128.0} y={cy + 170.0} width="80" height="70" rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="2" />
                        <text x={cx(1.0) + 168.0} y={cy + 214.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"2"</text>
                        <rect x={cx(1.0) + 218.0} y={cy + 170.0} width="80" height="70" rx="10" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="2" />
                        <text x={cx(1.0) + 258.0} y={cy + 214.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3"</text>
                        <text x={cx(1.0) + cw / 2.0} y={cy + 340.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"shape = [3]"</text>
                        <text x={cx(1.0) + cw / 2.0} y={cy + 372.0} font-family={FONT} font-size="15" fill={TEXT_MUTED} text-anchor="middle">"ndim = 1"</text>
                        <text x={cx(1.0) + cw / 2.0} y={cy + 440.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"список чисел:"</text>
                        <text x={cx(1.0) + cw / 2.0} y={cy + 464.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"ціни, оцінки"</text>
                        <text x={cx(1.0) + cw / 2.0} y={cy + 520.0} font-family={FONT} font-size="13" fill={COLOR_CYAN} text-anchor="middle">"tensor([1, 2, 3])"</text>
                    </g>
                </g>

                // ---- Card 2D ----
                <g opacity={g_alpha}>
                    <rect x={cx(2.0)} y={cy} width={cw} height={ch} rx="18" fill={CARD_BG} stroke={if a2 > 0.5 { COLOR_CYAN } else { CARD_BORDER }} stroke-width={if a2 > 0.5 { 2.5 } else { 1.5 }} />
                    <rect x={cx(2.0) + 20.0} y={cy + 20.0} width="180" height="30" rx="8" fill="#1e293b" />
                    <text x={cx(2.0) + 32.0} y={cy + 40.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN}>"2D: МАТРИЦЯ"</text>
                    <g opacity={a2}>
                        <rect x={cx(2.0) + 63.0} y={cy + 120.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <rect x={cx(2.0) + 133.0} y={cy + 120.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <rect x={cx(2.0) + 203.0} y={cy + 120.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <rect x={cx(2.0) + 63.0} y={cy + 176.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <rect x={cx(2.0) + 133.0} y={cy + 176.0} width="70" height="56" rx="8" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="2.5" />
                        <rect x={cx(2.0) + 203.0} y={cy + 176.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <rect x={cx(2.0) + 63.0} y={cy + 232.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <rect x={cx(2.0) + 133.0} y={cy + 232.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <rect x={cx(2.0) + 203.0} y={cy + 232.0} width="70" height="56" rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={cx(2.0) + cw / 2.0} y={cy + 340.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"shape = [3, 3]"</text>
                        <text x={cx(2.0) + cw / 2.0} y={cy + 372.0} font-family={FONT} font-size="15" fill={TEXT_MUTED} text-anchor="middle">"ndim = 2, осі: рядки × стовпці"</text>
                        <text x={cx(2.0) + cw / 2.0} y={cy + 440.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"таблиця даних"</text>
                        <text x={cx(2.0) + cw / 2.0} y={cy + 520.0} font-family={FONT} font-size="13" fill={COLOR_CYAN} text-anchor="middle">"torch.zeros(3, 3)"</text>
                    </g>
                </g>

                // ---- Card 3D ----
                <g opacity={g_alpha}>
                    <rect x={cx(3.0)} y={cy} width={cw} height={ch} rx="18" fill={CARD_BG} stroke={if a3 > 0.5 { COLOR_EMERALD } else { CARD_BORDER }} stroke-width={if a3 > 0.5 { 2.5 } else { 1.5 }} />
                    <rect x={cx(3.0) + 20.0} y={cy + 20.0} width="200" height="30" rx="8" fill="#1e293b" />
                    <text x={cx(3.0) + 32.0} y={cy + 40.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD}>"3D: RGB ЗОБРАЖЕННЯ"</text>
                    <g opacity={a3}>
                        <rect x={cx(3.0) + 83.0} y={cy + 110.0} width="170" height="60" rx="8" fill="#7f1d1d" stroke={COLOR_ROSE} stroke-width="2" />
                        <text x={cx(3.0) + 168.0} y={cy + 146.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"R канал"</text>
                        <rect x={cx(3.0) + 83.0} y={cy + 178.0} width="170" height="60" rx="8" fill="#14532d" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={cx(3.0) + 168.0} y={cy + 214.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"G канал"</text>
                        <rect x={cx(3.0) + 83.0} y={cy + 246.0} width="170" height="60" rx="8" fill="#1e3a8a" stroke={COLOR_CYAN} stroke-width="2" />
                        <text x={cx(3.0) + 168.0} y={cy + 282.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"B канал"</text>
                        <text x={cx(3.0) + cw / 2.0} y={cy + 340.0} font-family={FONT} font-size="20" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"shape = [3, H, W]"</text>
                        <text x={cx(3.0) + cw / 2.0} y={cy + 372.0} font-family={FONT} font-size="15" fill={TEXT_MUTED} text-anchor="middle">"ndim = 3"</text>
                        <text x={cx(3.0) + cw / 2.0} y={cy + 440.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"висота × ширина"</text>
                        <text x={cx(3.0) + cw / 2.0} y={cy + 464.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"× 3 кольори"</text>
                        <text x={cx(3.0) + cw / 2.0} y={cy + 520.0} font-family={FONT} font-size="13" fill={COLOR_EMERALD} text-anchor="middle">"пікселі 0-255 → [0,1]"</text>
                    </g>
                </g>

                // ---- Card 4D ----
                <g opacity={g_alpha}>
                    <rect x={cx(4.0)} y={cy} width={cw} height={ch} rx="18" fill={CARD_BG} stroke={if a4 > 0.5 { COLOR_EMERALD } else { CARD_BORDER }} stroke-width={if a4 > 0.5 { 2.5 } else { 1.5 }} />
                    <rect x={cx(4.0) + 20.0} y={cy + 20.0} width="200" height="30" rx="8" fill="#1e293b" />
                    <text x={cx(4.0) + 32.0} y={cy + 40.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD}>"4D: БАТЧ [B,C,H,W]"</text>
                    <g opacity={a4}>
                        <rect x={cx(4.0) + 58.0} y={cy + 100.0} width="220" height="80" rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x={cx(4.0) + 168.0} y={cy + 146.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"зображення 1"</text>
                        <rect x={cx(4.0) + 58.0} y={cy + 190.0} width="220" height="80" rx="10" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" stroke-dasharray="7 5" />
                        <text x={cx(4.0) + 168.0} y={cy + 236.0} font-family={FONT} font-size="15" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"зображення 2"</text>
                        <text x={cx(4.0) + 168.0} y={cy + 292.0} font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">"… × B"</text>
                        <text x={cx(4.0) + cw / 2.0} y={cy + 340.0} font-family={FONT} font-size="19" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"shape = [B,C,H,W]"</text>
                        <text x={cx(4.0) + cw / 2.0} y={cy + 372.0} font-family={FONT} font-size="15" fill={TEXT_MUTED} text-anchor="middle">"ndim = 4"</text>
                        <text x={cx(4.0) + cw / 2.0} y={cy + 440.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"мережі їдять батчами"</text>
                        <text x={cx(4.0) + cw / 2.0} y={cy + 464.0} font-family={FONT} font-size="14" fill={TEXT_DIM} text-anchor="middle">"напр. [16, 3, 224, 224]"</text>
                        <text x={cx(4.0) + cw / 2.0} y={cy + 520.0} font-family={FONT} font-size="13" fill={COLOR_EMERALD} text-anchor="middle">"DataLoader → батч"</text>
                    </g>
                </g>

                // ---- Bottom status bar ----
                <g opacity={g_alpha}>
                    <rect x="70" y="825" width="1780" height="185" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g transform="translate(110, 860)">
                        <text x="0" y="0" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_INDIGO} letter-spacing="1.0">"ЛІЧИЛЬНИК ВИМІРІВ: КОЖНА ВІСЬ = НОВИЙ РІВЕНЬ"</text>
                        <text x="0" y="44" font-family={FONT} font-size="26" font-weight="700" fill={COLOR_CYAN}>{format!("ndim = {}   shape = {}", ndim, cur_shape)}</text>
                        <text x="0" y="76" font-family={FONT} font-size="15" fill={TEXT_MAIN}>{cur_ex}</text>
                    </g>
                    <g transform="translate(1250, 855)">
                        <rect x="0" y="0" width="560" height="125" rx="12" fill="#0c4a6e" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x="280" y="32" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">"ПРАВИЛО: tensor.ndim = len(shape)"</text>
                        <text x="280" y="60" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"5D [B,C,D,H,W] — батч 3D-сканів"</text>
                        <text x="280" y="86" font-family={FONT} font-size="14" fill={TEXT_MAIN} text-anchor="middle">"(МРТ, КТ): глибина D + простір"</text>
                    </g>
                </g>
            </svg>
        )
    }
}
