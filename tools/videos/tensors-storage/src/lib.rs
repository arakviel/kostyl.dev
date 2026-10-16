//! Storage + Strides + Views: one buffer [1..6], View A [2,3] s=[3,1],
//! View B [3,2] s=[2,1]; transpose breaks contiguity -> reshape fix.
//! 10s loop, dark theme.

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

/// Triangular pulse centered at `at` with half-width `w`.
#[inline]
fn pulse(t: f32, at: f32, w: f32) -> f32 {
    clamp(1.0 - ((t - at).abs() / w), 0.0, 1.0)
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
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.2)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(6.2)..AudioTimestamp::Eof)
                .gain_db(0.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(7.4)..AudioTimestamp::Eof)
                .gain_db(-1.0),
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

        // Phase A pulses: storage cell k lights at 1.2 + k*0.35
        let pa = [
            pulse(t, 1.20, 0.45),
            pulse(t, 1.55, 0.45),
            pulse(t, 1.90, 0.45),
            pulse(t, 2.25, 0.45),
            pulse(t, 2.60, 0.45),
            pulse(t, 2.95, 0.45),
        ];
        // Phase B pulses at 4.2 + k*0.3
        let pb = [
            pulse(t, 4.20, 0.42),
            pulse(t, 4.50, 0.42),
            pulse(t, 4.80, 0.42),
            pulse(t, 5.10, 0.42),
            pulse(t, 5.40, 0.42),
            pulse(t, 5.70, 0.42),
        ];
        let phase_a_on = clamp((t - 1.0) / 0.5, 0.0, 1.0);
        let phase_b_on = clamp((t - 4.0) / 0.5, 0.0, 1.0);
        // Transpose error + fix badges
        let err_op = clamp((t - 6.2) / 0.5, 0.0, 1.0) * clamp((7.4 - t) / 0.5 + 1.0, 0.0, 1.0).min(1.0);
        let fix_op = clamp((t - 7.2) / 0.6, 0.0, 1.0);

        // Storage strip geometry
        let scw = 180.0;
        let sch = 92.0;
        let sgap = 16.0;
        let sx0 = (1920.0 - (6.0 * scw + 5.0 * sgap)) / 2.0;
        let sy = 210.0;
        let sx = |k: f32| sx0 + k * (scw + sgap);

        // View A grid (2x3) inside left card
        let ax0 = 150.0;
        let ay0 = 470.0;
        let acw = 130.0;
        let ach = 74.0;
        let ag = 12.0;
        let apos = |r: i32, c: i32| {
            (
                ax0 + c as f32 * (acw + ag),
                ay0 + r as f32 * (ach + ag),
            )
        };
        // View B grid (3x2)
        let bx0 = 1110.0;
        let by0 = 440.0;
        let bcw = 150.0;
        let bch = 66.0;
        let bpos = |r: i32, c: i32| {
            (
                bx0 + c as f32 * (bcw + ag),
                by0 + r as f32 * (bch + ag),
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
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={WIDTH / 2} cy={HEIGHT / 2} r="800" fill="url(#bg-glow)" />

                <g opacity={g_alpha}>
                    <rect x="600" y="24" width="720" height="32" rx="16" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="45" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "ПАМ'ЯТЬ ТЕНЗОРА: STORAGE + SHAPE + STRIDES"
                    </text>
                    <text x="960" y="92" font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Один буфер [1..6] — два різні погляди без копіювання"
                    </text>
                    <text x="960" y="126" font-family={FONT} font-size="16" fill={TEXT_MUTED} text-anchor="middle">
                        "View A: shape [2,3], strides [3,1]  →  View B: shape [3,2], strides [2,1]"
                    </text>
                </g>

                // ---- Storage strip ----
                <g opacity={g_alpha}>
                    <text x="960" y="190" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_DIM} text-anchor="middle" letter-spacing="1.0">
                        "STORAGE: ФІЗИЧНИЙ 1D-БУФЕР У ПАМ'ЯТІ (6 ЕЛЕМЕНТІВ)"
                    </text>
                    <rect x={sx(0.0)} y={sy} width={scw} height={sch} rx="10" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                    <text x={sx(0.0) + scw / 2.0} y={sy + 58.0} font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"1"</text>
                    <rect x={sx(0.0)} y={sy} width={scw} height={sch} rx="10" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[0].max(pb[0])} />
                    <rect x={sx(1.0)} y={sy} width={scw} height={sch} rx="10" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                    <text x={sx(1.0) + scw / 2.0} y={sy + 58.0} font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"2"</text>
                    <rect x={sx(1.0)} y={sy} width={scw} height={sch} rx="10" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[1].max(pb[1])} />
                    <rect x={sx(2.0)} y={sy} width={scw} height={sch} rx="10" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                    <text x={sx(2.0) + scw / 2.0} y={sy + 58.0} font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3"</text>
                    <rect x={sx(2.0)} y={sy} width={scw} height={sch} rx="10" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[2].max(pb[2])} />
                    <rect x={sx(3.0)} y={sy} width={scw} height={sch} rx="10" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                    <text x={sx(3.0) + scw / 2.0} y={sy + 58.0} font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"4"</text>
                    <rect x={sx(3.0)} y={sy} width={scw} height={sch} rx="10" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[3].max(pb[3])} />
                    <rect x={sx(4.0)} y={sy} width={scw} height={sch} rx="10" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                    <text x={sx(4.0) + scw / 2.0} y={sy + 58.0} font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"5"</text>
                    <rect x={sx(4.0)} y={sy} width={scw} height={sch} rx="10" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[4].max(pb[4])} />
                    <rect x={sx(5.0)} y={sy} width={scw} height={sch} rx="10" fill="#1e293b" stroke={TEXT_DIM} stroke-width="1.5" />
                    <text x={sx(5.0) + scw / 2.0} y={sy + 58.0} font-family={FONT} font-size="30" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"6"</text>
                    <rect x={sx(5.0)} y={sy} width={scw} height={sch} rx="10" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[5].max(pb[5])} />
                    <text x="960" y="330" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="middle">"offset(i,j) = i*stride[0] + j*stride[1] — та сама пам'ять, різна адресація"</text>
                </g>

                // ---- View A card ----
                <g opacity={g_alpha}>
                    <rect x="70" y="370" width="880" height="300" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="95" y="390" width="430" height="30" rx="8" fill="#1e293b" />
                    <text x="110" y="410" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.0">
                        "VIEW A: SHAPE [2,3], STRIDES [3,1] — CONTIGUOUS"
                    </text>
                    // rows: (0,0..2)=1,2,3 ; (1,0..2)=4,5,6
                    <g opacity={phase_a_on}>
                        <rect x={apos(0, 0).0} y={apos(0, 0).1} width={acw} height={ach} rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={apos(0, 0).0 + acw / 2.0} y={apos(0, 0).1 + 48.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"1"</text>
                        <rect x={apos(0, 0).0} y={apos(0, 0).1} width={acw} height={ach} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[0]} />
                        <rect x={apos(0, 1).0} y={apos(0, 1).1} width={acw} height={ach} rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={apos(0, 1).0 + acw / 2.0} y={apos(0, 1).1 + 48.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"2"</text>
                        <rect x={apos(0, 1).0} y={apos(0, 1).1} width={acw} height={ach} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[1]} />
                        <rect x={apos(0, 2).0} y={apos(0, 2).1} width={acw} height={ach} rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={apos(0, 2).0 + acw / 2.0} y={apos(0, 2).1 + 48.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3"</text>
                        <rect x={apos(0, 2).0} y={apos(0, 2).1} width={acw} height={ach} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[2]} />
                        <rect x={apos(1, 0).0} y={apos(1, 0).1} width={acw} height={ach} rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={apos(1, 0).0 + acw / 2.0} y={apos(1, 0).1 + 48.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"4"</text>
                        <rect x={apos(1, 0).0} y={apos(1, 0).1} width={acw} height={ach} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[3]} />
                        <rect x={apos(1, 1).0} y={apos(1, 1).1} width={acw} height={ach} rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={apos(1, 1).0 + acw / 2.0} y={apos(1, 1).1 + 48.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"5"</text>
                        <rect x={apos(1, 1).0} y={apos(1, 1).1} width={acw} height={ach} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[4]} />
                        <rect x={apos(1, 2).0} y={apos(1, 2).1} width={acw} height={ach} rx="8" fill="#1e293b" stroke={COLOR_CYAN} stroke-width="1.5" />
                        <text x={apos(1, 2).0 + acw / 2.0} y={apos(1, 2).1 + 48.0} font-family={FONT} font-size="26" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"6"</text>
                        <rect x={apos(1, 2).0} y={apos(1, 2).1} width={acw} height={ach} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pa[5]} />
                    </g>
                    <text x="700" y="470" font-family={FONT} font-size="13" fill={TEXT_DIM}>"x.view(3,2) OK — байти йдуть підряд"</text>
                </g>

                // ---- View B card ----
                <g opacity={g_alpha}>
                    <rect x="990" y="370" width="860" height="300" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="1015" y="390" width="430" height="30" rx="8" fill="#1e293b" />
                    <text x="1030" y="410" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD} letter-spacing="1.0">
                        "VIEW B: SHAPE [3,2], STRIDES [2,1] — ТАКОЖ VIEW"
                    </text>
                    <g opacity={phase_b_on}>
                        <rect x={bpos(0, 0).0} y={bpos(0, 0).1} width={bcw} height={bch} rx="8" fill="#1e293b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x={bpos(0, 0).0 + bcw / 2.0} y={bpos(0, 0).1 + 44.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"1"</text>
                        <rect x={bpos(0, 0).0} y={bpos(0, 0).1} width={bcw} height={bch} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pb[0]} />
                        <rect x={bpos(0, 1).0} y={bpos(0, 1).1} width={bcw} height={bch} rx="8" fill="#1e293b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x={bpos(0, 1).0 + bcw / 2.0} y={bpos(0, 1).1 + 44.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"2"</text>
                        <rect x={bpos(0, 1).0} y={bpos(0, 1).1} width={bcw} height={bch} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pb[1]} />
                        <rect x={bpos(1, 0).0} y={bpos(1, 0).1} width={bcw} height={bch} rx="8" fill="#1e293b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x={bpos(1, 0).0 + bcw / 2.0} y={bpos(1, 0).1 + 44.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"3"</text>
                        <rect x={bpos(1, 0).0} y={bpos(1, 0).1} width={bcw} height={bch} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pb[2]} />
                        <rect x={bpos(1, 1).0} y={bpos(1, 1).1} width={bcw} height={bch} rx="8" fill="#1e293b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x={bpos(1, 1).0 + bcw / 2.0} y={bpos(1, 1).1 + 44.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"4"</text>
                        <rect x={bpos(1, 1).0} y={bpos(1, 1).1} width={bcw} height={bch} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pb[3]} />
                        <rect x={bpos(2, 0).0} y={bpos(2, 0).1} width={bcw} height={bch} rx="8" fill="#1e293b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x={bpos(2, 0).0 + bcw / 2.0} y={bpos(2, 0).1 + 44.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"5"</text>
                        <rect x={bpos(2, 0).0} y={bpos(2, 0).1} width={bcw} height={bch} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pb[4]} />
                        <rect x={bpos(2, 1).0} y={bpos(2, 1).1} width={bcw} height={bch} rx="8" fill="#1e293b" stroke={COLOR_EMERALD} stroke-width="1.5" />
                        <text x={bpos(2, 1).0 + bcw / 2.0} y={bpos(2, 1).1 + 44.0} font-family={FONT} font-size="24" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">"6"</text>
                        <rect x={bpos(2, 1).0} y={bpos(2, 1).1} width={bcw} height={bch} rx="8" fill="none" stroke={COLOR_AMBER} stroke-width="3" opacity={pb[5]} />
                    </g>
                    <text x="1560" y="470" font-family={FONT} font-size="13" fill={TEXT_DIM}>"той самий data_ptr — zero-copy"</text>
                </g>

                // ---- Bottom: transpose trap + fix ----
                <g opacity={g_alpha}>
                    <rect x="70" y="695" width="1780" height="315" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g opacity={err_op}>
                        <rect x="110" y="720" width="820" height="110" rx="12" fill="#4c0519" stroke={COLOR_ROSE} stroke-width="2" />
                        <text x="520" y="758" font-family={FONT} font-size="17" font-weight="700" fill={COLOR_ROSE} text-anchor="middle">"ПАСТКА: t = x.t() → is_contiguous = False"</text>
                        <text x="520" y="792" font-family={FONT} font-size="15" fill={TEXT_MAIN} text-anchor="middle">"t.view(2, 3) → RuntimeError (байти не підряд)"</text>
                    </g>
                    <g opacity={fix_op}>
                        <rect x="990" y="720" width="820" height="110" rx="12" fill="#064e3b" stroke={COLOR_EMERALD} stroke-width="2" />
                        <text x="1400" y="758" font-family={FONT} font-size="17" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">"ФІКС: reshape АБО contiguous().view()"</text>
                        <text x="1400" y="792" font-family={FONT} font-size="15" fill={TEXT_MAIN} text-anchor="middle">"t.reshape(2,3) — універсально; .contiguous() копіює"</text>
                    </g>
                    <g transform="translate(110, 870)">
                        <text x="0" y="0" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_INDIGO} letter-spacing="1.0">"ПРАВИЛО ПАМ'ЯТІ: VIEW vs RESHAPE vs CLONE"</text>
                        <text x="0" y="34" font-family={FONT} font-size="16" fill={TEXT_MAIN}>"view(): без копії, лише contiguous  |  reshape(): сам вирішує  |  clone(): новий буфер"</text>
                        <text x="0" y="64" font-family={FONT} font-size="15" fill={TEXT_MUTED}>"is_contiguous() — перевірка перед view  |  detach() ділить буфер, clone().detach() — ізоляція"</text>
                        <text x="0" y="94" font-family={FONT} font-size="15" fill={TEXT_DIM}>"in-place add_() мутує буфер: економія VRAM, але ризик для autograd"</text>
                    </g>
                </g>
            </svg>
        )
    }
}
