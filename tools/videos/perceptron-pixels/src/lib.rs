//! Visualization of the perceptron pixel-weight intuition.
//!
//! "Each pixel is a brightness number. Multiply each pixel by its importance weight,
//! sum them up, and get a similarity score for a digit."
use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct PerceptronPixelsMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

// Palette
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

// 8x8 input image (digit "0")
const DIGIT_0: [f32; 64] = [
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
    0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
    0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,
    0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
];

// 8x8 weights template for digit "0" (detector mask)
const WEIGHTS_0: [f32; 64] = [
   -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,
   -0.5, -0.2,  1.5,  1.5,  1.5,  1.5, -0.2, -0.5,
   -0.5,  1.5,  1.5, -1.8, -1.8,  1.5,  1.5, -0.5,
   -0.5,  1.5,  1.5, -1.8, -1.8,  1.5,  1.5, -0.5,
   -0.5,  1.5,  1.5, -1.8, -1.8,  1.5,  1.5, -0.5,
   -0.5,  1.5,  1.5, -1.8, -1.8,  1.5,  1.5, -0.5,
   -0.5, -0.2,  1.5,  1.5,  1.5,  1.5, -0.2, -0.5,
   -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,
];

pub struct PerceptronPixelsVideo<'a> {
    pub media: &'a PerceptronPixelsMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> PerceptronPixelsVideo<'a> {
    pub fn new(media: &'a PerceptronPixelsMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for PerceptronPixelsVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PerceptronPixelsVideo").finish()
    }
}

impl fframes::Video for PerceptronPixelsVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(10.5)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("scan.wav", AudioTimestamp::Second(3.2)..AudioTimestamp::Eof).gain_db(-2.0),
            AudioTrack::new("chime.wav", AudioTimestamp::Second(7.2)..AudioTimestamp::Eof).gain_db(0.0),
        ])
    }

    fn render_frame<'a>(&'a self, frame: Frame, _ctx: &FFramesContext<'a, '_>) -> Svgr<'a> {
        let t = frame.seconds();

        // Coordinates
        let cell_size = 42.0_f32;
        let cell_gap = 5.0_f32;
        let total_grid_w = 8.0_f32 * (cell_size + cell_gap) - cell_gap;

        // Left Grid (Pixels X)
        let g1_x = 120.0_f32;
        let g1_y = 295.0_f32;

        // Middle Grid (Weights W)
        let g2_x = 660.0_f32;
        let g2_y = 295.0_f32;

        // Right Card (Score & Evaluation)
        let card3_x = 1200.0_f32;
        let card3_y = 205.0_f32;
        let card3_w = 600.0_f32;
        let card3_h = 670.0_f32;

        // Timings & Phases
        let intro_alpha = ease_out_cubic(clamp(t / 1.0, 0.0, 1.0));

        // Scan Sweep (Phase 2): 3.2s -> 5.8s
        let scan_t = clamp((t - 3.2) / 2.6, 0.0, 1.0);
        let scan_col = scan_t * 8.0_f32;
        let is_scanning = t >= 3.2 && t <= 6.2;

        // Summation Accumulation follows the scan: 3.2s -> 6.2s
        let sum_p = ease_out_cubic(scan_t);
        let current_score = 25.0 * sum_p;

        // Recognition Verdict (Phase 4): 7.2s -> 9.6s
        let is_recognized = t >= 7.2 && t < 10.0;
        let chime_t = clamp((t - 7.2) / 1.2, 0.0, 1.0);
        let rip_r = 70.0 + 80.0 * chime_t;
        let rip_alpha = (1.0 - chime_t) * 0.85;

        // Smooth loop reset: 9.6s -> 10.5s
        let loop_reset = if t >= 9.6 {
            1.0 - ease_in_out(clamp((t - 9.6) / 0.9, 0.0, 1.0))
        } else {
            1.0
        };

        // Phase tracking
        let current_phase = if t < 2.0 {
            1
        } else if t < 3.2 {
            2
        } else if t < 7.2 {
            3
        } else {
            4
        };

        let (phase_title, phase_desc) = match current_phase {
            1 => ("ФАЗА 1: КОЖЕН ПІКСЕЛЬ — ЦЕ ЧИСЛО", "Матриця яскравості зображення: xi = 1.0 (контур цифри), xi = 0.0 (порожній фон)"),
            2 => ("ФАЗА 2: ВАГИ ВАЖЛИВОСТІ (ДЕТЕКТОР ОЗНАК)", "wi > 0 (зелені) — очікуваний контур нуля; wi < 0 (червоні) — заборонений центр"),
            3 => ("ФАЗА 3: СКАНУВАННЯ ТА ПОЕЛЕМЕНТНИЙ ДОБУТОК", "Обчислення добутку xi · wi для кожного пікселя та накопичення суми схожості"),
            _ => ("ФАЗА 4: ПІДСУМКОВА ОЦІНКА СХОЖОСТІ", "Сума z = +25.0 значно перевищує поріг 0. Цифра «0» успішно розпізнана (ŷ = 1)!"),
        };

        // Precompute Grid Cells as Vec<Svgr<'a>>
        let pixel_cells: Vec<Svgr<'a>> = (0..64)
            .map(|i| {
                let r = i / 8;
                let c = i % 8;
                let px_x = c as f32 * (cell_size + cell_gap);
                let px_y = r as f32 * (cell_size + cell_gap);
                let val = DIGIT_0[i];

                let (cell_fill, text_color, border_color) = if val > 0.5 {
                    ("#0284c7", TEXT_MAIN, "#38bdf8")
                } else {
                    ("#0b1329", TEXT_DIM, "#1e293b")
                };

                fframes::svgr!(
                    <g>
                        <rect x={px_x} y={px_y} width={cell_size} height={cell_size} rx="6" fill={cell_fill} stroke={border_color} stroke-width="1.5" />
                        <text x={px_x + cell_size / 2.0} y={px_y + cell_size / 2.0 + 5.0} font-family={FONT} font-size="12" font-weight="700" fill={text_color} text-anchor="middle">
                            {if val > 0.5 { "1.0" } else { "0" }}
                        </text>
                    </g>
                )
            })
            .collect();

        let weight_cells: Vec<Svgr<'a>> = (0..64)
            .map(|i| {
                let r = i / 8;
                let c = i % 8;
                let px_x = c as f32 * (cell_size + cell_gap);
                let px_y = r as f32 * (cell_size + cell_gap);
                let w = WEIGHTS_0[i];

                let (cell_fill, text_color, border_color) = if w > 1.0 {
                    ("#064e3b", "#34d399", "#10b981")
                } else if w < -1.0 {
                    ("#4c0519", "#fda4af", "#f43f5e")
                } else if w < 0.0 {
                    ("#26121b", "#fb7185", "#881337")
                } else {
                    ("#0f172a", TEXT_DIM, "#1e293b")
                };

                fframes::svgr!(
                    <g>
                        <rect x={px_x} y={px_y} width={cell_size} height={cell_size} rx="6" fill={cell_fill} stroke={border_color} stroke-width="1.5" />
                        <text x={px_x + cell_size / 2.0} y={px_y + cell_size / 2.0 + 5.0} font-family={FONT} font-size="11" font-weight="700" fill={text_color} text-anchor="middle">
                            {format!("{:.1}", w)}
                        </text>
                    </g>
                )
            })
            .collect();

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <radialGradient id="bg-glow" cx="0.5" cy="0.4" r="0.6">
                        <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.4" />
                        <stop offset="60%" stop-color="#0b1329" stop-opacity="0.15" />
                        <stop offset="100%" stop-color={BG_COLOR} stop-opacity="0" />
                    </radialGradient>

                    <radialGradient id="win-glow" cx="0.5" cy="0.5" r="0.5">
                        <stop offset="0%" stop-color="#10b981" stop-opacity={format!("{:.2}", if is_recognized { 0.45 * loop_reset } else { 0.0 })} />
                        <stop offset="100%" stop-color="#10b981" stop-opacity="0" />
                    </radialGradient>

                    <pattern id="dot-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="1.2" fill="#334155" opacity="0.3" />
                    </pattern>
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH as f32 / 2.0} cy={HEIGHT as f32 / 2.0} r="750" fill="url(#bg-glow)" />

                <g opacity={intro_alpha}>
                    <rect x="740" y="32" width="440" height="34" rx="17" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="54" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "ІНТУЇЦІЯ ПЕРСЕПТРОНА: ОБРОБКА ЗОБРАЖЕНЬ (1957)"
                    </text>

                    <text x="960" y="106" font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Пікселі як числа • Ваги як важливість • Сума як оцінка схожості"
                    </text>

                    <text x="960" y="142" font-family={FONT} font-size="18" fill={TEXT_MUTED} text-anchor="middle">
                        "Як перший штучний нейрон Розенблатта розпізнає рукописну цифру «0» через лінійну зважену суму"
                    </text>
                </g>

                <g opacity={intro_alpha}>
                    <rect x="80" y="205" width="450" height="670" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    
                    <rect x="110" y="235" width="220" height="30" rx="8" fill="#1e293b" />
                    <text x="220" y="255" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        "1. ВХІДНЕ ЗОБРАЖЕННЯ (X)"
                    </text>
                    <text x="220" y="280" font-family={FONT} font-size="13" fill={TEXT_MUTED} text-anchor="middle">
                        "Сітка 8x8 = 64 пікселі (x1..x64)"
                    </text>

                    <g transform={format!("translate({}, {})", g1_x, g1_y)}>
                        {pixel_cells}
                    </g>

                    <rect x="110" y="700" width="390" height="74" rx="10" fill="#1e293b" stroke="#334155" stroke-width="1" />
                    <text x="305" y="728" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Вхід: цифра «0»"
                    </text>
                    <text x="305" y="752" font-family={FONT} font-size="13" fill={COLOR_CYAN} text-anchor="middle">
                        "20 активних пікселів контуру (xi = 1.0)"
                    </text>
                </g>

                <g opacity={intro_alpha}>
                    <circle cx="595" cy="480" r="32" fill="#1e293b" stroke="#334155" stroke-width="2" />
                    <text x="595" y="491" font-family={FONT} font-size="32" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">
                        "×"
                    </text>
                    <text x="595" y="534" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_MUTED} text-anchor="middle">
                        "множимо"
                    </text>
                </g>

                <g opacity={intro_alpha}>
                    <rect x="620" y="205" width="450" height="670" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    
                    <rect x="650" y="235" width="220" height="30" rx="8" fill="#1e293b" />
                    <text x="760" y="255" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                        "2. ШАБЛОН ВАГ (W)"
                    </text>
                    <text x="760" y="280" font-family={FONT} font-size="13" fill={TEXT_MUTED} text-anchor="middle">
                        "Ваги детектора цифри «0» (w1..w64)"
                    </text>

                    <g transform={format!("translate({}, {})", g2_x, g2_y)}>
                        {weight_cells}
                    </g>

                    <rect x="650" y="700" width="390" height="74" rx="10" fill="#1e293b" stroke="#334155" stroke-width="1" />
                    <text x="845" y="728" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Зелені (+1.5): контур цифри"
                    </text>
                    <text x="845" y="752" font-family={FONT} font-size="13" fill={COLOR_ROSE} text-anchor="middle">
                        "Червоні (-1.8): штраф за зайвий центр"
                    </text>
                </g>

                <g opacity={intro_alpha}>
                    <circle cx="1135" cy="480" r="32" fill="#1e293b" stroke="#334155" stroke-width="2" />
                    <text x="1135" y="490" font-family={FONT} font-size="28" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        "Σ"
                    </text>
                    <text x="1135" y="534" font-family={FONT} font-size="13" font-weight="700" fill={TEXT_MUTED} text-anchor="middle">
                        "сумуємо"
                    </text>
                </g>

                {
                    if is_scanning {
                        let sx1 = g1_x + (scan_col * (cell_size + cell_gap)).min(total_grid_w);
                        let sx2 = g2_x + (scan_col * (cell_size + cell_gap)).min(total_grid_w);
                        fframes::svgr!(
                            <g>
                                <line x1={sx1} y1={g1_y - 10.0} x2={sx1} y2={g1_y + total_grid_w + 10.0} stroke={COLOR_CYAN} stroke-width="3" opacity="0.8" />
                                <line x1={sx2} y1={g2_y - 10.0} x2={sx2} y2={g2_y + total_grid_w + 10.0} stroke={COLOR_EMERALD} stroke-width="3" opacity="0.8" />
                            </g>
                        )
                    } else {
                        fframes::svgr!(<g></g>)
                    }
                }

                <g opacity={intro_alpha}>
                    <rect x={card3_x} y={card3_y} width={card3_w} height={card3_h} rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    
                    <rect x={card3_x + 30.0} y="235" width="260" height="30" rx="8" fill="#1e293b" />
                    <text x={card3_x + 160.0} y="255" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                        "3. ОЦІНКА СХОЖОСТІ (СКОР)"
                    </text>

                    <g transform={format!("translate({}, 290)", card3_x + 30.0)}>
                        <rect x="0" y="0" width="540" height="110" rx="12" fill="#1e293b" stroke="#334155" stroke-width="1" />
                        
                        <text x="270" y="30" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_CYAN} text-anchor="middle">
                            "z = ∑ (xi · wi) + b"
                        </text>

                        <text x="270" y="60" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                            "20 пікселів збігу: 20 × (+1.5) = +30.0"
                        </text>
                        <text x="270" y="85" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                            "Центр порожній: 0 штрафу • Зсув (b): -5.0"
                        </text>
                    </g>

                    <g transform={format!("translate({}, 425)", card3_x + 30.0)}>
                        <rect x="0" y="0" width="540" height="145" rx="14" fill="#0b1329" stroke={if is_recognized { COLOR_EMERALD } else { "#334155" }} stroke-width="2" />
                        
                        <text x="270" y="35" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_MUTED} text-anchor="middle">
                            "СУМАРНИЙ СКОР СХОЖОСТІ (z)"
                        </text>

                        <text x="270" y="90" font-family={FONT} font-size="48" font-weight="700" fill={if is_recognized { COLOR_EMERALD } else { COLOR_CYAN }} text-anchor="middle">
                            {format!("{:+05.1}", current_score * loop_reset)}
                        </text>

                        <text x="270" y="125" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                            {if current_score >= 15.0 { "ПОРОГ ПЕРЕВИЩЕНО (z ≥ 0) -> ВИСОКА СХОЖІСТЬ!" } else { "РОЗРАХУНОК СУМИ..." }}
                        </text>
                    </g>

                    <g transform={format!("translate({}, 595)", card3_x + 30.0)}>
                        {
                            if is_recognized && rip_alpha > 0.01 {
                                fframes::svgr!(
                                    <circle cx="270" cy="85" r={rip_r} fill="none" stroke={COLOR_EMERALD} stroke-width="3" opacity={format!("{:.2}", rip_alpha)} />
                                )
                            } else {
                                fframes::svgr!(<g></g>)
                            }
                        }

                        <rect x="0" y="0" width="540" height="170" rx="14" fill={if is_recognized { "#064e3b" } else { "#1e293b" }} stroke={if is_recognized { COLOR_EMERALD } else { "#334155" }} stroke-width="2" />
                        
                        <circle cx="270" cy="85" r="75" fill="url(#win-glow)" />

                        <text x="270" y="45" font-family={FONT} font-size="16" font-weight="700" fill={if is_recognized { "#a7f3d0" } else { TEXT_DIM }} text-anchor="middle">
                            "ВЕРДИКТ ПЕРСЕПТРОНА"
                        </text>

                        <text x="270" y="95" font-family={FONT} font-size="34" font-weight="700" fill={if is_recognized { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            {if is_recognized { "ЦЕ ЦИФРА «0»!" } else { "ОЧІКУВАННЯ..." }}
                        </text>

                        <text x="270" y="135" font-family={FONT} font-size="16" font-weight="700" fill={if is_recognized { COLOR_EMERALD } else { TEXT_DIM }} text-anchor="middle">
                            {if is_recognized { "ŷ = Step(z) = 1 (Розпізнано з високою точністю)" } else { "ŷ = ?" }}
                        </text>
                    </g>
                </g>

                <g opacity={intro_alpha} transform="translate(80, 895)">
                    <rect x="0" y="0" width="1760" height="135" rx="16" fill="#0f172a" stroke="#1e293b" stroke-width="1.5" />

                    <g transform="translate(40, 24)">
                        <rect x="0" y="0" width="390" height="32" rx="8" fill={if current_phase == 1 { "#0369a1" } else { "#1e293b" }} />
                        <text x="195" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 1 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "1. Пікселі (яскравість)"
                        </text>

                        <rect x="420" y="0" width="390" height="32" rx="8" fill={if current_phase == 2 { "#065f46" } else { "#1e293b" }} />
                        <text x="615" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 2 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "2. Ваги важливості"
                        </text>

                        <rect x="840" y="0" width="390" height="32" rx="8" fill={if current_phase == 3 { "#0284c7" } else { "#1e293b" }} />
                        <text x="1035" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 3 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "3. Множення & Сума Σ"
                        </text>

                        <rect x="1260" y="0" width="420" height="32" rx="8" fill={if current_phase == 4 { "#059669" } else { "#1e293b" }} />
                        <text x="1470" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if current_phase == 4 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "4. Оцінка схожості (ŷ = 1)"
                        </text>
                    </g>

                    <text x="50" y="86" font-family={FONT} font-size="16" font-weight="700" fill={COLOR_CYAN}>
                        {phase_title}
                    </text>
                    <text x="50" y="112" font-family={FONT} font-size="15" fill={TEXT_MUTED}>
                        {phase_desc}
                    </text>

                    <text x="1710" y="100" font-family={FONT} font-size="15" font-weight="700" fill={TEXT_DIM} text-anchor="end">
                        {format!("Час: {:.1}c / 10.5c  •  Кадр {}", t, frame.index)}
                    </text>
                </g>
            </svg>
        )
    }
}
