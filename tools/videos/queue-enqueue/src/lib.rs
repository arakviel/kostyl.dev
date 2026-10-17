//! Queue (стаття 89): анатомія операції enqueue на кільцевому буфері.
//!
//! Timeline (14s, 16:9, dark):
//! 0.0-1.4   intro fade (порожня черга: front_=0, rear_=-1, size_=0)
//! 1.4-4.55  три enqueue: rear_ обертається, записи [0]=12, [1]=7, [2]=41
//! 4.55-6.65 два dequeue: front_ обертається, слоти [0] та [1] звільняються
//! 6.65-11.9 чотири enqueue: rear_ 2->3->4->5 і WRAP-AROUND (5+1)%6=0 -> слот [0]=8,
//!           потім слот [1] перезаписується (57) — size_=6, черга повна
//! 11.9-13.3 спроба enqueue(97): isFull()=true -> throw std::overflow_error
//! 13.3-14.0 seamless loop fade

use fframes::{
    AudioMap, AudioTimestamp, AudioTrack, Color, Duration, FFramesContext, Frame, Svgr,
    include_media_dir,
};

include_media_dir!(pub struct QueueEnqueueMedia, "media");

pub const WIDTH: usize = 1920;
pub const HEIGHT: usize = 1080;

const FONT: &str = "Arial";

// Palette (kostyl.dev dark)
const BG_COLOR: &str = "#070b14";
const CARD_BG: &str = "#0f172a";
const CARD_BORDER: &str = "#1e293b";
const TEXT_MAIN: &str = "#f8fafc";
const TEXT_MUTED: &str = "#94a3b8";
const TEXT_DIM: &str = "#64748b";
const CODE_PLAIN: &str = "#cbd5e1";

const COLOR_CYAN: &str = "#38bdf8";
const COLOR_INDIGO: &str = "#818cf8";
const COLOR_AMBER: &str = "#f59e0b";
const COLOR_EMERALD: &str = "#10b981";
const COLOR_ROSE: &str = "#f43f5e";

// Ring geometry
const CX: f32 = 560.0;
const CY: f32 = 560.0;
const R_RING: f32 = 230.0; // радіус до центрів слотів
const R_PTR: f32 = 336.0; // радіус бейджів front/rear
const SLOT_W: f32 = 118.0;
const SLOT_H: f32 = 72.0;

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
fn ease_out_back(t: f32) -> f32 {
    let t = clamp(t, 0.0, 1.0);
    let c1 = 1.70158f32;
    let c3 = c1 + 1.0;
    1.0 + c3 * (t - 1.0).powi(3) + c1 * (t - 1.0).powi(2)
}

// Квадратична крива Безьє
#[inline]
fn quad(p0: (f32, f32), c: (f32, f32), p1: (f32, f32), t: f32) -> (f32, f32) {
    let u = 1.0 - t;
    (
        u * u * p0.0 + 2.0 * u * t * c.0 + t * t * p1.0,
        u * u * p0.1 + 2.0 * u * t * c.1 + t * t * p1.1,
    )
}

const DOCK_IN: (f32, f32) = (830.0, 240.0); // док "виробник" enqueue
const DOCK_OUT: (f32, f32) = (300.0, 240.0); // док "споживач" dequeue

pub struct QueueEnqueueVideo<'a> {
    pub media: &'a QueueEnqueueMedia,
    #[allow(dead_code)]
    title: String,
}

impl<'a> QueueEnqueueVideo<'a> {
    pub fn new(media: &'a QueueEnqueueMedia, title: &str) -> Self {
        Self {
            media,
            title: title.to_string(),
        }
    }
}

impl std::fmt::Debug for QueueEnqueueVideo<'_> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("QueueEnqueueVideo").finish()
    }
}

impl fframes::Video for QueueEnqueueVideo<'_> {
    const FPS: usize = 30;
    const WIDTH: usize = WIDTH;
    const HEIGHT: usize = HEIGHT;
    const BACKGROUND_COLOR: Color = Color::rgb(7, 11, 20);

    fn duration(&self) -> Duration<'_> {
        Duration::Seconds(14.0)
    }

    fn audio(&self) -> AudioMap<'_> {
        AudioMap::from([
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(1.94)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(2.99)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.04)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(4.70)..AudioTimestamp::Eof)
                .gain_db(-4.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(5.75)..AudioTimestamp::Eof)
                .gain_db(-4.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(7.19)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(8.24)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(9.29)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(10.34)..AudioTimestamp::Eof)
                .gain_db(-3.0),
            AudioTrack::new("pulse.wav", AudioTimestamp::Second(11.39)..AudioTimestamp::Eof)
                .gain_db(-2.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(10.05)..AudioTimestamp::Eof)
                .gain_db(-1.0),
            AudioTrack::new("activate.wav", AudioTimestamp::Second(12.30)..AudioTimestamp::Eof)
                .gain_db(0.0),
        ])
    }

    fn render_frame<'a>(&'a self, frame: Frame, _ctx: &FFramesContext<'a, '_>) -> Svgr<'a> {
        let t = frame.seconds();

        let intro_alpha = ease_out_cubic(clamp(t / 1.2, 0.0, 1.0));
        let loop_reset = if t >= 13.25 {
            1.0 - ease_in_out(clamp((t - 13.25) / 0.75, 0.0, 1.0))
        } else {
            1.0
        };
        let g_alpha = intro_alpha * loop_reset;
        let header_dy = (1.0 - intro_alpha) * -16.0;

        // ---- лічильник size_ (значення за подіями запису/видалення) ----
        let count_ev: [(f32, i32); 10] = [
            (1.94, 1),
            (2.99, 2),
            (4.04, 3),
            (4.99, 2),
            (6.04, 1),
            (7.19, 2),
            (8.24, 3),
            (9.29, 4),
            (10.34, 5),
            (11.39, 6),
        ];
        let count: i32 = count_ev
            .iter()
            .rev()
            .find(|(te, _)| t >= *te)
            .map(|(_, c)| *c)
            .unwrap_or(0);

        // пульс лічильника + спливання "+1/-1"
        let mut count_pulse = 0.0f32;
        let mut float_d = f32::MAX;
        let mut float_up = true;
        for (i, (te, c)) in count_ev.iter().enumerate() {
            let prev = if i == 0 { 0 } else { count_ev[i - 1].1 };
            if *c != prev {
                let d = t - te;
                if d >= 0.0 && d < 0.65 {
                    count_pulse = count_pulse.max(1.0 - d / 0.65);
                    float_d = d;
                    float_up = *c > prev;
                }
            }
        }
        let count_scale = 1.0 + 0.16 * count_pulse;
        let full = count >= 6;

        // ---- кути покажчиків front/rear (0° = слот [0] зверху, 60° на слот) ----
        let rear_th: f32 = if t < 1.4 {
            -60.0
        } else if t < 1.85 {
            -60.0 + 60.0 * ease_in_out(clamp((t - 1.4) / 0.45, 0.0, 1.0))
        } else if t < 2.45 {
            0.0
        } else if t < 2.9 {
            0.0 + 60.0 * ease_in_out(clamp((t - 2.45) / 0.45, 0.0, 1.0))
        } else if t < 3.5 {
            60.0
        } else if t < 3.95 {
            60.0 + 60.0 * ease_in_out(clamp((t - 3.5) / 0.45, 0.0, 1.0))
        } else if t < 6.65 {
            120.0
        } else if t < 7.1 {
            120.0 + 60.0 * ease_in_out(clamp((t - 6.65) / 0.45, 0.0, 1.0))
        } else if t < 7.7 {
            180.0
        } else if t < 8.15 {
            180.0 + 60.0 * ease_in_out(clamp((t - 7.7) / 0.45, 0.0, 1.0))
        } else if t < 8.75 {
            240.0
        } else if t < 9.2 {
            240.0 + 60.0 * ease_in_out(clamp((t - 8.75) / 0.45, 0.0, 1.0))
        } else if t < 9.8 {
            300.0
        } else if t < 10.25 {
            300.0 + 60.0 * ease_in_out(clamp((t - 9.8) / 0.45, 0.0, 1.0)) // WRAP 5 -> 0
        } else if t < 10.85 {
            360.0
        } else if t < 11.3 {
            360.0 + 60.0 * ease_in_out(clamp((t - 10.85) / 0.45, 0.0, 1.0))
        } else {
            420.0
        };
        let rear_display: i32 = if t < 1.4 {
            -1
        } else if t < 2.45 {
            0
        } else if t < 3.5 {
            1
        } else if t < 6.65 {
            2
        } else if t < 7.7 {
            3
        } else if t < 8.75 {
            4
        } else if t < 9.8 {
            5
        } else if t < 10.85 {
            0
        } else {
            1
        };
        let rear_ghost = t < 1.4;

        let front_th: f32 = if t < 5.15 {
            0.0
        } else if t < 5.5 {
            0.0 + 60.0 * ease_in_out(clamp((t - 5.15) / 0.35, 0.0, 1.0))
        } else if t < 6.2 {
            60.0
        } else if t < 6.55 {
            60.0 + 60.0 * ease_in_out(clamp((t - 6.2) / 0.35, 0.0, 1.0))
        } else {
            120.0
        };
        let front_display: i32 = if t < 5.5 {
            0
        } else if t < 6.55 {
            1
        } else {
            2
        };

        // ---- геометрія слотів ----
        let c2 = 0.866_025_4_f32;
        let slot_x: [f32; 6] = [
            CX,
            CX + R_RING * c2,
            CX + R_RING * c2,
            CX,
            CX - R_RING * c2,
            CX - R_RING * c2,
        ];
        let slot_y: [f32; 6] = [
            CY - R_RING,
            CY - R_RING * 0.5,
            CY + R_RING * 0.5,
            CY + R_RING,
            CY + R_RING * 0.5,
            CY - R_RING * 0.5,
        ];

        // ---- стани слотів (слот, значення, колір, появи, звільнення) ----
        let events_data: [(usize, &'static str, &'static str, f32, Option<f32>); 8] = [
            (0, "12", COLOR_CYAN, 1.94, Some(4.70)),
            (0, "8", COLOR_CYAN, 10.34, None),
            (1, "7", COLOR_INDIGO, 2.99, Some(5.75)),
            (1, "57", COLOR_INDIGO, 11.39, None),
            (2, "41", COLOR_AMBER, 4.04, None),
            (3, "23", COLOR_CYAN, 7.19, None),
            (4, "99", COLOR_INDIGO, 8.24, None),
            (5, "56", COLOR_AMBER, 9.29, None),
        ];
        let mut slot_val: [&str; 6] = ["", "", "", "", "", ""];
        let mut slot_col: [&str; 6] = [CARD_BORDER; 6];
        let mut slot_born: [f32; 6] = [0.0; 6];
        for &(i, v, col, b, d) in &events_data {
            let dd = d.unwrap_or(f32::MAX);
            if t >= b && t < dd {
                slot_val[i] = v;
                slot_col[i] = col;
                slot_born[i] = b;
            }
        }
        let mut slot_occ = [0.0f32; 6];
        let mut slot_free_flash = [0.0f32; 6];
        for i in 0..6 {
            if !slot_val[i].is_empty() {
                slot_occ[i] = clamp((t - slot_born[i]) / 0.35, 0.0, 1.0);
            }
        }
        for &(i, d0) in &[(0usize, 4.70f32), (1, 5.75f32)] {
            let d = t - d0;
            if d >= 0.0 && d < 0.5 {
                slot_free_flash[i] = 1.0 - d / 0.5;
            }
        }

        // ---- летючий чип enqueue ----
        let enq_ops: [(f32, &'static str, usize); 8] = [
            (1.4, "12", 0),
            (2.45, "7", 1),
            (3.5, "41", 2),
            (6.65, "23", 3),
            (7.7, "99", 4),
            (8.75, "56", 5),
            (9.8, "8", 0),
            (10.85, "57", 1),
        ];
        let mut chip_x = 0.0f32;
        let mut chip_y = 0.0f32;
        let mut chip_val = "";
        let mut chip_op = 0.0f32;
        for &(t0, v, slot) in &enq_ops {
            let f0 = t0 + 0.21;
            let f1 = t0 + 0.54;
            if t >= f0 && t < f1 {
                let p = ease_in_out((t - f0) / 0.33);
                let target = (slot_x[slot], slot_y[slot]);
                let ctrl = (
                    (DOCK_IN.0 + target.0) / 2.0,
                    (290.0 + target.1) / 2.0 - 105.0,
                );
                let (qx, qy) = quad(DOCK_IN, ctrl, target, p);
                chip_x = qx;
                chip_y = qy;
                chip_val = v;
                chip_op = clamp((t - f0) / 0.08, 0.0, 1.0);
                break;
            }
        }
        let chip_lab = match chip_val {
            "12" => "enqueue(12)",
            "7" => "enqueue(7)",
            "41" => "enqueue(41)",
            "23" => "enqueue(23)",
            "99" => "enqueue(99)",
            "56" => "enqueue(56)",
            "8" => "enqueue(8)",
            "57" => "enqueue(57)",
            _ => "",
        };
        let chip_col = match chip_val {
            "12" | "23" | "8" => COLOR_CYAN,
            "7" | "99" | "57" => COLOR_INDIGO,
            "41" | "56" => COLOR_AMBER,
            _ => COLOR_CYAN,
        };

        // ---- летючий чип dequeue ----
        let deq_ops: [(f32, &'static str, usize); 2] = [(4.55, "12", 0), (5.6, "7", 1)];
        let mut dchip_x = 0.0f32;
        let mut dchip_y = 0.0f32;
        let mut dchip_val = "";
        let mut dchip_op = 0.0f32;
        for &(t0, v, slot) in &deq_ops {
            let f0 = t0 + 0.15;
            let f1 = t0 + 0.55;
            if t >= f0 && t < f1 {
                let p = ease_in_out((t - f0) / 0.4);
                let target = (DOCK_OUT.0, DOCK_OUT.1 + 34.0);
                let ctrl = (
                    (slot_x[slot] + target.0) / 2.0,
                    (slot_y[slot] + target.1) / 2.0 - 120.0,
                );
                let (qx, qy) = quad((slot_x[slot], slot_y[slot]), ctrl, target, p);
                dchip_x = qx;
                dchip_y = qy;
                dchip_val = v;
                dchip_op = clamp((t - f0) / 0.08, 0.0, 1.0) * clamp((f1 - t) / 0.12, 0.0, 1.0);
                break;
            }
        }

        // ---- заблокований чип overflow-спроби ----
        let ovf_show = t >= 11.95 && t < 13.0;
        let (ovf_x, ovf_y) = if t < 12.25 {
            quad(
                DOCK_IN,
                (770.0, 300.0),
                (710.0, 375.0),
                ease_in_out(clamp((t - 11.95) / 0.3, 0.0, 1.0)),
            )
        } else {
            quad(
                (710.0, 375.0),
                (770.0, 300.0),
                DOCK_IN,
                ease_in_out(clamp((t - 12.25) / 0.3, 0.0, 1.0)),
            )
        };
        let ovf_alpha = if t < 12.25 {
            clamp((t - 11.95) / 0.1, 0.0, 1.0)
        } else {
            1.0 - clamp((t - 12.55) / 0.35, 0.0, 1.0)
        };
        let ovf_throw = t >= 12.25;
        let ovf_throw_p = clamp((t - 12.25) / 0.4, 0.0, 1.0);

        // тремтіння кільця під час throw
        let shake_dx = if t >= 12.25 && t < 12.8 {
            let d = (t - 12.25) / 0.55;
            ((t - 12.25) * 55.0).sin() * 7.0 * (1.0 - d)
        } else {
            0.0
        };

        // ---- підсвічення рядків коду ----
        let marks: [(f32, i32); 31] = [
            (0.0, -1),
            (1.4, 4),
            (1.94, 5),
            (2.24, 6),
            (2.45, 4),
            (2.99, 5),
            (3.29, 6),
            (3.5, 4),
            (4.04, 5),
            (4.34, 6),
            (4.55, 104),
            (5.3, 105),
            (5.6, 104),
            (6.35, 105),
            (6.65, 4),
            (7.19, 5),
            (7.49, 6),
            (7.7, 4),
            (8.24, 5),
            (8.54, 6),
            (8.75, 4),
            (9.29, 5),
            (9.59, 6),
            (9.8, 4),
            (10.34, 5),
            (10.64, 6),
            (10.85, 4),
            (11.39, 5),
            (11.69, 6),
            (11.9, 2),
            (12.6, 3),
        ];
        let active_line: i32 = marks
            .iter()
            .rev()
            .find(|(te, _)| t >= *te)
            .map(|(_, l)| *l)
            .unwrap_or(-1);

        // а-опистості тіл enqueue/dequeue (кросфейд при зміні)
        let a_enq: f32 = if t < 4.4 {
            1.0
        } else if t < 4.7 {
            1.0 - (t - 4.4) / 0.3
        } else if t < 6.5 {
            0.0
        } else if t < 6.8 {
            (t - 6.5) / 0.3
        } else {
            1.0
        };
        let a_deq: f32 = 1.0 - a_enq;

        // ---- поточний виклик для шапки панелі коду ----
        let call = if t < 1.4 {
            "очікування виклику..."
        } else if t < 2.45 {
            "enqueue(12)"
        } else if t < 3.5 {
            "enqueue(7)"
        } else if t < 4.55 {
            "enqueue(41)"
        } else if t < 6.65 {
            "dequeue()"
        } else if t < 7.7 {
            "enqueue(23)"
        } else if t < 8.75 {
            "enqueue(99)"
        } else if t < 9.8 {
            "enqueue(56)"
        } else if t < 10.85 {
            "enqueue(8) — WRAP"
        } else if t < 11.9 {
            "enqueue(57) — останній слот"
        } else {
            "enqueue(97) — переповнення"
        };

        // ---- фази ----
        let phase: usize = if t < 1.4 {
            1
        } else if t < 4.55 {
            2
        } else if t < 6.65 {
            3
        } else if t < 11.9 {
            4
        } else {
            5
        };
        let phase_title = match phase {
            1 => "Порожня черга на кільцевому буфері",
            2 => "enqueue: заповнення з кінця (FIFO)",
            3 => "dequeue: вилучення з початку (FIFO)",
            4 => "Wrap-around: rear_ обертається за модулем",
            _ => "Переповнення: контракт захищає буфер",
        };
        let phase_desc = match phase {
            1 => "front_ = 0, rear_ = -1, size_ = 0 — наступний вільний rear_ = (rear_ + 1) % capacity_ = 0",
            2 => "Передумова isFull() = false -> rear_ = (rear_ + 1) % 6, запис data_[rear_], ++size_",
            3 => "Передумова isEmpty() = false -> front_ = (front_ + 1) % 6, --size_; звільнений слот чекає rear_",
            4 => "rear_ = (5 + 1) % 6 = 0: слот [0] перезаписано — жодного зсуву елементів, усе за O(1)",
            5 => "isFull() = true -> throw std::overflow_error(\"Queue overflow: cannot enqueue to full queue\")",
            _ => "",
        };
        let phase_accent = match phase {
            1 => TEXT_MUTED,
            2 => COLOR_CYAN,
            3 => COLOR_EMERALD,
            4 => COLOR_AMBER,
            _ => COLOR_ROSE,
        };

        let wrap_arc_op = if t >= 9.8 && t < 11.7 {
            clamp((t - 9.8) / 0.2, 0.0, 1.0) * (1.0 - clamp((t - 11.2) / 0.5, 0.0, 1.0))
        } else {
            0.0
        };
        let full_flash = if full { 0.5 + 0.5 * ((t - 11.39) * 4.0).sin().abs() } else { 0.0 };
        let throw_flash = if ovf_throw {
            1.0 - clamp((t - 12.25) / 0.55, 0.0, 1.0)
        } else {
            0.0
        };

        let badge_pill_h = 40.0f32;
        let badge_tri_h = 14.0f32;

        // білборд-бейджі: пілюля горизонтальна (текст не обертається), трикутник дивиться в центр
        // коли front і rear вказують на один слот — розсуваємо їх радіально
        let same_slot = rear_display >= 0 && rear_display == front_display;
        let rear_r = if same_slot { 372.0 } else { R_PTR };
        let front_r = if same_slot { 300.0 } else { R_PTR };
        let a_rear = (rear_th - 90.0).to_radians();
        let rear_bx = CX + rear_r * a_rear.cos();
        let rear_by = CY + rear_r * a_rear.sin();
        let rear_rot = a_rear.to_degrees() + 90.0;
        let a_front = (front_th - 90.0).to_radians();
        let front_bx = CX + front_r * a_front.cos();
        let front_by = CY + front_r * a_front.sin();
        let front_rot = a_front.to_degrees() + 90.0;

        fframes::svgr!(
            <svg xmlns="http://www.w3.org/2000/svg" viewBox={format!("0 0 {WIDTH} {HEIGHT}")} width={WIDTH} height={HEIGHT}>
                <defs>
                    <radialGradient id="bg-glow" cx="0.5" cy="0.5" r="0.55">
                        <stop offset="0%" stop-color="#1e1b4b" stop-opacity="0.35" />
                        <stop offset="60%" stop-color="#0b1329" stop-opacity="0.10" />
                        <stop offset="100%" stop-color={BG_COLOR} stop-opacity="0" />
                    </radialGradient>
                    <radialGradient id="panel-glow" cx="0.5" cy="0.5" r="0.5">
                        <stop offset="0%" stop-color="#0284c7" stop-opacity="0.08" />
                        <stop offset="100%" stop-color="#0f172a" stop-opacity="0" />
                    </radialGradient>
                    <pattern id="dot-grid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <circle cx="20" cy="20" r="1.2" fill="#334155" opacity="0.25" />
                    </pattern>
                </defs>

                <rect width={WIDTH} height={HEIGHT} fill={BG_COLOR} />
                <rect width={WIDTH} height={HEIGHT} fill="url(#dot-grid)" />
                <circle cx={CX} cy={CY} r="640" fill="url(#bg-glow)" />
                <circle cx={1400.0} cy={540.0} r="430" fill="url(#panel-glow)" />

                <text x="36" y="38" font-family={FONT} font-size="13" fill={TEXT_DIM} opacity={g_alpha}>
                    "kostyl.dev"
                </text>

                // ================= ШАПКА =================
                <g opacity={g_alpha} transform={format!("translate(0 {:.1})", header_dy)}>
                    <rect x="620" y="26" width="680" height="34" rx="17" fill="#0f172a" stroke="#0284c7" stroke-width="1.5" />
                    <text x="960" y="48" font-family={FONT} font-size="14" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1.5">
                        "СТРУКТУРИ ДАНИХ • C++ • ЧЕРГА (QUEUE) • КІЛЬЦЕВИЙ БУФЕР"
                    </text>
                    <text x="960" y="104" font-family={FONT} font-size="34" font-weight="700" fill={TEXT_MAIN} text-anchor="middle">
                        "Черга (Queue): анатомія enqueue на кільцевому буфері"
                    </text>
                    <text x="960" y="142" font-family={FONT} font-size="17" fill={TEXT_MUTED} text-anchor="middle">
                        "FIFO: enqueue — в кінець (rear_), dequeue — з початку (front_); індекси обертаються: i = (i + 1) % capacity_"
                    </text>
                </g>

                // ================= ДОКИ ВИРОБНИК/СПОЖИВАЧ =================
                <g opacity={g_alpha}>
                    <circle cx={DOCK_IN.0} cy={DOCK_IN.1} r="30" fill="none" stroke={COLOR_CYAN} stroke-width="1.5" stroke-dasharray="6 5" opacity={format!("{:.2}", 0.45 + 0.25 * ((t * 2.0).sin().abs()))} />
                    <text x={DOCK_IN.0} y={DOCK_IN.1 - 42.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} text-anchor="middle" letter-spacing="1">
                        "ВИРОБНИК: enqueue(v)"
                    </text>
                    <circle cx={DOCK_OUT.0} cy={DOCK_OUT.1} r="30" fill="none" stroke={COLOR_EMERALD} stroke-width="1.5" stroke-dasharray="6 5" opacity={format!("{:.2}", 0.45 + 0.25 * ((t * 2.0 + 1.3).sin().abs()))} />
                    <text x={DOCK_OUT.0} y={DOCK_OUT.1 - 42.0} font-family={FONT} font-size="13" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle" letter-spacing="1">
                        "СПОЖИВАЧ: dequeue()"
                    </text>
                </g>

                // ================= КІЛЬЦЕВИЙ БУФЕР =================
                <g opacity={g_alpha} transform={format!("translate({:.2} 0)", shake_dx)}>
                    // жила кільця
                    <circle cx={CX} cy={CY} r={R_RING} fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 14" opacity="0.2" />
                    {
                        let ring_extra = throw_flash.max(full_flash * 0.6);
                        if ring_extra > 0.01 {
                            fframes::svgr!(
                                <circle cx={CX} cy={CY} r={R_RING} fill="none" stroke={if throw_flash > 0.0 { COLOR_ROSE } else { COLOR_AMBER }} stroke-width={format!("{:.1}", 2.5 + 2.5 * ring_extra)} stroke-dasharray="4 14" opacity={format!("{:.2}", 0.7 * ring_extra)} />
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    // дуга wrap-around (210° -> 270°)
                    {
                        if wrap_arc_op > 0.01 {
                            fframes::svgr!(
                                <g>
                                    <path d="M 269 392 A 336 336 0 0 1 560 224" fill="none" stroke={COLOR_AMBER} stroke-width="5" stroke-linecap="round" opacity={format!("{:.2}", wrap_arc_op * 0.9)} />
                                    <text x="372" y="250" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_AMBER} text-anchor="middle" opacity={format!("{:.2}", wrap_arc_op)}>
                                        "(5 + 1) % 6 = 0"
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    // стрілки напрямку обертання (за годинниковою стрілкою)
                    <g transform={format!("translate({:.1} {:.1}) rotate(30)", CX + 115.0, CY - 199.2)} opacity="0.5">
                        <path d="M -9 -9 L 7 0 L -9 9" fill="none" stroke={TEXT_MUTED} stroke-width="2.5" stroke-linecap="round" />
                    </g>
                    <g transform={format!("translate({:.1} {:.1}) rotate(90)", CX + 230.0, CY)} opacity="0.5">
                        <path d="M -9 -9 L 7 0 L -9 9" fill="none" stroke={TEXT_MUTED} stroke-width="2.5" stroke-linecap="round" />
                    </g>
                    <g transform={format!("translate({:.1} {:.1}) rotate(150)", CX + 115.0, CY + 199.2)} opacity="0.5">
                        <path d="M -9 -9 L 7 0 L -9 9" fill="none" stroke={TEXT_MUTED} stroke-width="2.5" stroke-linecap="round" />
                    </g>
                    <g transform={format!("translate({:.1} {:.1}) rotate(210)", CX - 115.0, CY + 199.2)} opacity="0.5">
                        <path d="M -9 -9 L 7 0 L -9 9" fill="none" stroke={TEXT_MUTED} stroke-width="2.5" stroke-linecap="round" />
                    </g>
                    <g transform={format!("translate({:.1} {:.1}) rotate(270)", CX - 230.0, CY)} opacity="0.5">
                        <path d="M -9 -9 L 7 0 L -9 9" fill="none" stroke={TEXT_MUTED} stroke-width="2.5" stroke-linecap="round" />
                    </g>
                    <g transform={format!("translate({:.1} {:.1}) rotate(330)", CX - 115.0, CY - 199.2)} opacity="0.5">
                        <path d="M -9 -9 L 7 0 L -9 9" fill="none" stroke={TEXT_MUTED} stroke-width="2.5" stroke-linecap="round" />
                    </g>

                    // ================= СЛОТИ [0..5] =================
                    // слот [0] (верх)
                    <g>
                        {
                            if slot_free_flash[0] > 0.01 {
                                fframes::svgr!(
                                    <rect x={slot_x[0] - SLOT_W / 2.0} y={slot_y[0] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16" fill="none" stroke={COLOR_ROSE} stroke-width="3" opacity={format!("{:.2}", slot_free_flash[0] * 0.8)} />
                                )
                            } else {
                                fframes::svgr!(<g></g>)
                            }
                        }
                        {
                            let occ = !slot_val[0].is_empty();
                            let sc = 0.75 + 0.25 * ease_out_back(slot_occ[0]);
                            fframes::svgr!(
                                <g>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <circle cx={slot_x[0]} cy={slot_y[0]} r={format!("{:.1}", 34.0 + 70.0 * (1.0 - slot_occ[0]))} fill={slot_col[0]} opacity="0.18" />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <rect x={slot_x[0] - SLOT_W / 2.0} y={slot_y[0] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16"
                                        fill={if occ { slot_col[0] } else { CARD_BG }}
                                        fill-opacity={if occ { format!("{:.2}", 0.16 * slot_occ[0].max(0.15)) } else { "1".to_string() }}
                                        stroke={if !occ && slot_free_flash[0] > 0.01 { COLOR_ROSE } else if occ { slot_col[0] } else { CARD_BORDER }}
                                        stroke-width={if occ || slot_free_flash[0] > 0.01 { "2.4" } else { "1.5" }} />
                                    <text x={slot_x[0]} y={slot_y[0] - 20.0} font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} text-anchor="middle">
                                        "[0]"
                                    </text>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <text x="0" y="9" font-family={FONT} font-size="26" font-weight="800" fill={TEXT_MAIN} text-anchor="middle" transform={format!("translate({:.1} {:.1}) scale({:.3})", slot_x[0], slot_y[0] + 6.0, sc)}>
                                                    { slot_val[0] }
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }
                    </g>
                    // слот [1] (верх-право)
                    <g>
                        {
                            if slot_free_flash[1] > 0.01 {
                                fframes::svgr!(
                                    <rect x={slot_x[1] - SLOT_W / 2.0} y={slot_y[1] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16" fill="none" stroke={COLOR_ROSE} stroke-width="3" opacity={format!("{:.2}", slot_free_flash[1] * 0.8)} />
                                )
                            } else {
                                fframes::svgr!(<g></g>)
                            }
                        }
                        {
                            let occ = !slot_val[1].is_empty();
                            let sc = 0.75 + 0.25 * ease_out_back(slot_occ[1]);
                            fframes::svgr!(
                                <g>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <circle cx={slot_x[1]} cy={slot_y[1]} r={format!("{:.1}", 34.0 + 70.0 * (1.0 - slot_occ[1]))} fill={slot_col[1]} opacity="0.18" />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <rect x={slot_x[1] - SLOT_W / 2.0} y={slot_y[1] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16"
                                        fill={if occ { slot_col[1] } else { CARD_BG }}
                                        fill-opacity={if occ { format!("{:.2}", 0.16 * slot_occ[1].max(0.15)) } else { "1".to_string() }}
                                        stroke={if !occ && slot_free_flash[1] > 0.01 { COLOR_ROSE } else if occ { slot_col[1] } else { CARD_BORDER }}
                                        stroke-width={if occ || slot_free_flash[1] > 0.01 { "2.4" } else { "1.5" }} />
                                    <text x={slot_x[1]} y={slot_y[1] - 20.0} font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} text-anchor="middle">
                                        "[1]"
                                    </text>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <text x="0" y="9" font-family={FONT} font-size="26" font-weight="800" fill={TEXT_MAIN} text-anchor="middle" transform={format!("translate({:.1} {:.1}) scale({:.3})", slot_x[1], slot_y[1] + 6.0, sc)}>
                                                    { slot_val[1] }
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }
                    </g>
                    // слот [2] (низ-право)
                    <g>
                        {
                            let occ = !slot_val[2].is_empty();
                            let sc = 0.75 + 0.25 * ease_out_back(slot_occ[2]);
                            fframes::svgr!(
                                <g>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <circle cx={slot_x[2]} cy={slot_y[2]} r={format!("{:.1}", 34.0 + 70.0 * (1.0 - slot_occ[2]))} fill={slot_col[2]} opacity="0.18" />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <rect x={slot_x[2] - SLOT_W / 2.0} y={slot_y[2] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16"
                                        fill={if occ { slot_col[2] } else { CARD_BG }}
                                        fill-opacity={if occ { format!("{:.2}", 0.16 * slot_occ[2].max(0.15)) } else { "1".to_string() }}
                                        stroke={if occ { slot_col[2] } else { CARD_BORDER }}
                                        stroke-width={if occ { "2.4" } else { "1.5" }} />
                                    <text x={slot_x[2]} y={slot_y[2] - 20.0} font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} text-anchor="middle">
                                        "[2]"
                                    </text>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <text x="0" y="9" font-family={FONT} font-size="26" font-weight="800" fill={TEXT_MAIN} text-anchor="middle" transform={format!("translate({:.1} {:.1}) scale({:.3})", slot_x[2], slot_y[2] + 6.0, sc)}>
                                                    { slot_val[2] }
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }
                    </g>
                    // слот [3] (низ)
                    <g>
                        {
                            let occ = !slot_val[3].is_empty();
                            let sc = 0.75 + 0.25 * ease_out_back(slot_occ[3]);
                            fframes::svgr!(
                                <g>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <circle cx={slot_x[3]} cy={slot_y[3]} r={format!("{:.1}", 34.0 + 70.0 * (1.0 - slot_occ[3]))} fill={slot_col[3]} opacity="0.18" />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <rect x={slot_x[3] - SLOT_W / 2.0} y={slot_y[3] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16"
                                        fill={if occ { slot_col[3] } else { CARD_BG }}
                                        fill-opacity={if occ { format!("{:.2}", 0.16 * slot_occ[3].max(0.15)) } else { "1".to_string() }}
                                        stroke={if occ { slot_col[3] } else { CARD_BORDER }}
                                        stroke-width={if occ { "2.4" } else { "1.5" }} />
                                    <text x={slot_x[3]} y={slot_y[3] - 20.0} font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} text-anchor="middle">
                                        "[3]"
                                    </text>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <text x="0" y="9" font-family={FONT} font-size="26" font-weight="800" fill={TEXT_MAIN} text-anchor="middle" transform={format!("translate({:.1} {:.1}) scale({:.3})", slot_x[3], slot_y[3] + 6.0, sc)}>
                                                    { slot_val[3] }
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }
                    </g>
                    // слот [4] (низ-ліво)
                    <g>
                        {
                            let occ = !slot_val[4].is_empty();
                            let sc = 0.75 + 0.25 * ease_out_back(slot_occ[4]);
                            fframes::svgr!(
                                <g>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <circle cx={slot_x[4]} cy={slot_y[4]} r={format!("{:.1}", 34.0 + 70.0 * (1.0 - slot_occ[4]))} fill={slot_col[4]} opacity="0.18" />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <rect x={slot_x[4] - SLOT_W / 2.0} y={slot_y[4] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16"
                                        fill={if occ { slot_col[4] } else { CARD_BG }}
                                        fill-opacity={if occ { format!("{:.2}", 0.16 * slot_occ[4].max(0.15)) } else { "1".to_string() }}
                                        stroke={if occ { slot_col[4] } else { CARD_BORDER }}
                                        stroke-width={if occ { "2.4" } else { "1.5" }} />
                                    <text x={slot_x[4]} y={slot_y[4] - 20.0} font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} text-anchor="middle">
                                        "[4]"
                                    </text>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <text x="0" y="9" font-family={FONT} font-size="26" font-weight="800" fill={TEXT_MAIN} text-anchor="middle" transform={format!("translate({:.1} {:.1}) scale({:.3})", slot_x[4], slot_y[4] + 6.0, sc)}>
                                                    { slot_val[4] }
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }
                    </g>
                    // слот [5] (верх-ліво)
                    <g>
                        {
                            let occ = !slot_val[5].is_empty();
                            let sc = 0.75 + 0.25 * ease_out_back(slot_occ[5]);
                            fframes::svgr!(
                                <g>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <circle cx={slot_x[5]} cy={slot_y[5]} r={format!("{:.1}", 34.0 + 70.0 * (1.0 - slot_occ[5]))} fill={slot_col[5]} opacity="0.18" />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <rect x={slot_x[5] - SLOT_W / 2.0} y={slot_y[5] - SLOT_H / 2.0} width={SLOT_W} height={SLOT_H} rx="16"
                                        fill={if occ { slot_col[5] } else { CARD_BG }}
                                        fill-opacity={if occ { format!("{:.2}", 0.16 * slot_occ[5].max(0.15)) } else { "1".to_string() }}
                                        stroke={if occ { slot_col[5] } else { CARD_BORDER }}
                                        stroke-width={if occ { "2.4" } else { "1.5" }} />
                                    <text x={slot_x[5]} y={slot_y[5] - 20.0} font-family={FONT} font-size="12" font-weight="700" fill={TEXT_DIM} text-anchor="middle">
                                        "[5]"
                                    </text>
                                    {
                                        if occ {
                                            fframes::svgr!(
                                                <text x="0" y="9" font-family={FONT} font-size="26" font-weight="800" fill={TEXT_MAIN} text-anchor="middle" transform={format!("translate({:.1} {:.1}) scale({:.3})", slot_x[5], slot_y[5] + 6.0, sc)}>
                                                    { slot_val[5] }
                                                </text>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }
                    </g>

                    // ================= ЦЕНТР: size_ та isFull() =================
                    <text x={CX} y={CY - 62.0} font-family={FONT} font-size="16" font-weight="700" fill={TEXT_MUTED} text-anchor="middle" letter-spacing="1.5">
                        "size_"
                    </text>
                    <g transform={format!("translate({:.1} {:.1}) scale({:.3})", CX, CY + 14.0, count_scale)}>
                        <text x="0" y="0" font-family={FONT} font-size="62" font-weight="800" fill={if full { COLOR_AMBER } else { TEXT_MAIN }} text-anchor="middle">
                            { format!("{}", count) }
                        </text>
                    </g>
                    <text x={CX} y={CY + 48.0} font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="middle">
                        "з capacity_ = 6"
                    </text>
                    <rect x={CX - 92.0} y={CY + 64.0} width="184" height="30" rx="15"
                        fill={if full { COLOR_AMBER } else { "#0f172a" }}
                        fill-opacity={if full { format!("{:.2}", 0.12 + 0.08 * full_flash) } else { "1".to_string() }}
                        stroke={if full { COLOR_AMBER } else { "#1e293b" }} stroke-width="1.5" />
                    <text x={CX} y={CY + 84.0} font-family={FONT} font-size="14" font-weight="700" fill={if full { COLOR_AMBER } else { TEXT_MUTED }} text-anchor="middle">
                        { if full { "isFull(): TRUE" } else { "isFull(): false" } }
                    </text>
                    {
                        if float_d < 0.65 {
                            fframes::svgr!(
                                <g opacity={format!("{:.2}", (1.0 - float_d / 0.65) * 0.9)}>
                                    <text x={CX + 66.0} y={CY + 6.0 - ease_out_cubic(clamp(float_d / 0.65, 0.0, 1.0)) * 42.0} font-family={FONT} font-size="20" font-weight="800" fill={if float_up { COLOR_EMERALD } else { COLOR_ROSE }} text-anchor="middle">
                                        { if float_up { "+1" } else { "-1" } }
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    // ================= БЕЙДЖ rear_ (бурштиновий, білборд) =================
                    <g opacity={if rear_ghost { "0.35" } else { "1" }} transform={format!("translate({:.1} {:.1})", rear_bx, rear_by)}>
                        <rect x="-54" y={format!("{:.1}", -badge_pill_h / 2.0)} width="108" height={badge_pill_h} rx="20"
                            fill={COLOR_AMBER} fill-opacity={if rear_ghost { "0.06" } else { "0.14" }}
                            stroke={COLOR_AMBER} stroke-width="1.8" stroke-opacity={if rear_ghost { "0.5" } else { "1" }}
                            stroke-dasharray={if rear_ghost { "7 5" } else { "1 0" }} />
                        <text x="0" y="6.0" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_AMBER} text-anchor="middle">
                            { format!("rear_ = {}", rear_display) }
                        </text>
                    </g>
                    <g transform={format!("translate({:.1} {:.1}) rotate({:.2})", rear_bx, rear_by, rear_rot)}>
                        <polygon points={format!("-8,{:.1} 8,{:.1} 0,{:.1}", badge_pill_h / 2.0 + 2.0, badge_pill_h / 2.0 + 2.0, badge_pill_h / 2.0 + badge_tri_h + 2.0)}
                            fill={COLOR_AMBER} fill-opacity={if rear_ghost { "0.35" } else { "1" }} />
                    </g>

                    // ================= БЕЙДЖ front_ (смарагдовий, білборд) =================
                    <g transform={format!("translate({:.1} {:.1})", front_bx, front_by)}>
                        <rect x="-54" y={format!("{:.1}", -badge_pill_h / 2.0)} width="108" height={badge_pill_h} rx="20"
                            fill={COLOR_EMERALD} fill-opacity="0.14" stroke={COLOR_EMERALD} stroke-width="1.8" />
                        <text x="0" y="6.0" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD} text-anchor="middle">
                            { format!("front_ = {}", front_display) }
                        </text>
                    </g>
                    <g transform={format!("translate({:.1} {:.1}) rotate({:.2})", front_bx, front_by, front_rot)}>
                        <polygon points={format!("-8,{:.1} 8,{:.1} 0,{:.1}", badge_pill_h / 2.0 + 2.0, badge_pill_h / 2.0 + 2.0, badge_pill_h / 2.0 + badge_tri_h + 2.0)}
                            fill={COLOR_EMERALD} />
                    </g>

                    // ================= чип enqueue =================
                    {
                        if chip_op > 0.0 && !chip_val.is_empty() {
                            fframes::svgr!(
                                <g opacity={format!("{:.2}", chip_op)}>
                                    <circle cx={chip_x} cy={chip_y} r="38" fill={chip_col} opacity="0.14" />
                                    <rect x={chip_x - 33.0} y={chip_y - 25.0} width="66" height="50" rx="12" fill="#0f172a" stroke={chip_col} stroke-width="2.5" />
                                    <text x={chip_x} y={chip_y + 9.0} font-family={FONT} font-size="24" font-weight="800" fill={TEXT_MAIN} text-anchor="middle">
                                        { chip_val }
                                    </text>
                                    <text x={chip_x} y={chip_y + 64.0} font-family={FONT} font-size="12" font-weight="700" fill={chip_col} text-anchor="middle">
                                        { chip_lab }
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    // ================= чип dequeue =================
                    {
                        if dchip_op > 0.01 && !dchip_val.is_empty() {
                            fframes::svgr!(
                                <g opacity={format!("{:.2}", dchip_op)}>
                                    <circle cx={dchip_x} cy={dchip_y} r="38" fill={COLOR_ROSE} opacity="0.12" />
                                    <rect x={dchip_x - 33.0} y={dchip_y - 25.0} width="66" height="50" rx="12" fill="#0f172a" stroke={COLOR_ROSE} stroke-width="2.5" />
                                    <text x={dchip_x} y={dchip_y + 9.0} font-family={FONT} font-size="24" font-weight="800" fill={TEXT_MAIN} text-anchor="middle">
                                        { dchip_val }
                                    </text>
                                    <text x={dchip_x} y={dchip_y + 56.0} font-family={FONT} font-size="12" font-weight="700" fill={COLOR_ROSE} text-anchor="middle">
                                        "dequeue()"
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }

                    // ================= заблокований чип (overflow) =================
                    {
                        if ovf_show && ovf_alpha > 0.01 {
                            fframes::svgr!(
                                <g opacity={format!("{:.2}", ovf_alpha)}>
                                    <circle cx={ovf_x} cy={ovf_y} r="38" fill={if ovf_throw { COLOR_ROSE } else { COLOR_CYAN }} opacity="0.12" />
                                    <rect x={ovf_x - 33.0} y={ovf_y - 25.0} width="66" height="50" rx="12" fill="#0f172a" stroke={if ovf_throw { COLOR_ROSE } else { COLOR_CYAN }} stroke-width="2.5" />
                                    <text x={ovf_x} y={ovf_y + 9.0} font-family={FONT} font-size="24" font-weight="800" fill={if ovf_throw { COLOR_ROSE } else { TEXT_MAIN }} text-anchor="middle">
                                        "97"
                                    </text>
                                    <text x={ovf_x} y={ovf_y + 56.0} font-family={FONT} font-size="12" font-weight="700" fill={if ovf_throw { COLOR_ROSE } else { COLOR_CYAN }} text-anchor="middle">
                                        "enqueue(97)"
                                    </text>
                                    {
                                        if ovf_throw && ovf_throw_p < 1.0 {
                                            fframes::svgr!(
                                                <circle cx={ovf_x} cy={ovf_y} r={format!("{:.1}", 34.0 + 60.0 * ovf_throw_p)} fill="none" stroke={COLOR_ROSE} stroke-width="3" opacity={format!("{:.2}", (1.0 - ovf_throw_p) * 0.8)} />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }
                </g>

                // ================= ПАНЕЛЬ КОДУ =================
                <g opacity={g_alpha}>
                    <rect x="970" y="210" width="860" height="430" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="992" y="230" width="250" height="34" rx="8" fill="#1e293b" />
                    <text x="1010" y="253" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_CYAN} letter-spacing="1.2">
                        "QUEUE · ТІЛО ОПЕРАЦІЇ"
                    </text>
                    <rect x="1492" y="230" width="316" height="34" rx="8" fill="#1e293b" stroke={if t >= 11.9 { COLOR_ROSE } else { "#334155" }} stroke-width="1" />
                    <text x="1650" y="253" font-family={FONT} font-size="13" font-weight="700" fill={if t >= 11.9 { COLOR_ROSE } else { TEXT_MUTED }} text-anchor="middle">
                        { call }
                    </text>

                    // ----- тіло enqueue -----
                    <g opacity={format!("{:.2}", a_enq)}>
                        {
                            // L2 highlight (перевірка передумови)
                            let l2_active = active_line == 2;
                            fframes::svgr!(
                                <g>
                                    {
                                        if l2_active {
                                            fframes::svgr!(
                                                <rect x="992" y="336" width="816" height="32" rx="8" fill={COLOR_ROSE} opacity={format!("{:.2}", 0.22 + 0.12 * ((t * 7.0).sin().abs()))} />
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <text x="1010" y="318" font-family={FONT} font-size="19" font-weight={if active_line == 1 { "800" } else { "400" }} fill={if active_line == 1 { COLOR_CYAN } else { CODE_PLAIN }}>
                                        "void enqueue(int value)"
                                    </text>
                                    <text x="1010" y="358" font-family={FONT} font-size="19" font-weight={if l2_active { "800" } else { "400" }} fill={if l2_active { COLOR_ROSE } else { CODE_PLAIN }}>
                                        "if (isFull())"
                                    </text>
                                    <text x="1044" y="398" font-family={FONT} font-size="19" font-weight={if active_line == 3 { "800" } else { "400" }} fill={if active_line == 3 { COLOR_ROSE } else { CODE_PLAIN }}>
                                        "throw std::overflow_error(\"Queue overflow\");"
                                    </text>
                                </g>
                            )
                        }
                        {
                            // L4 highlight (обертання rear_) + WRAP-мітка
                            let l4_active = active_line == 4;
                            let wrap_mode = t >= 9.8 && t < 10.85;
                            fframes::svgr!(
                                <g>
                                    {
                                        if l4_active {
                                            fframes::svgr!(
                                                <g>
                                                    <rect x="992" y="416" width="816" height="32" rx="8" fill={if wrap_mode { COLOR_AMBER } else { "#0284c7" }} opacity={format!("{:.2}", if wrap_mode { 0.28 } else { 0.30 })} />
                                                    <rect x="992" y="416" width="4" height="32" rx="2" fill={if wrap_mode { COLOR_AMBER } else { COLOR_CYAN }} />
                                                </g>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <text x="1010" y="438" font-family={FONT} font-size="19" font-weight={if l4_active { "800" } else { "400" }} fill={if l4_active { if wrap_mode { COLOR_AMBER } else { COLOR_CYAN } } else { CODE_PLAIN }}>
                                        "rear_ = (rear_ + 1) % capacity_;"
                                    </text>
                                    {
                                        if wrap_mode {
                                            fframes::svgr!(
                                                <g>
                                                    <rect x="1500" y="420" width="100" height="24" rx="6" fill={COLOR_AMBER} fill-opacity="0.18" stroke={COLOR_AMBER} stroke-width="1" />
                                                    <text x="1550" y="437" font-family={FONT} font-size="12" font-weight="800" fill={COLOR_AMBER} text-anchor="middle">
                                                        "WRAP"
                                                    </text>
                                                </g>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                </g>
                            )
                        }
                        {
                            // L5 highlight (запис)
                            let l5_active = active_line == 5;
                            fframes::svgr!(
                                <g>
                                    {
                                        if l5_active {
                                            fframes::svgr!(
                                                <g>
                                                    <rect x="992" y="456" width="816" height="32" rx="8" fill="#0284c7" opacity="0.30" />
                                                    <rect x="992" y="456" width="4" height="32" rx="2" fill={COLOR_CYAN} />
                                                </g>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <text x="1010" y="478" font-family={FONT} font-size="19" font-weight={if l5_active { "800" } else { "400" }} fill={if l5_active { COLOR_CYAN } else { CODE_PLAIN }}>
                                        "data_[rear_] = value;"
                                    </text>
                                </g>
                            )
                        }
                        {
                            // L6 highlight (лічильник)
                            let l6_active = active_line == 6;
                            fframes::svgr!(
                                <g>
                                    {
                                        if l6_active {
                                            fframes::svgr!(
                                                <g>
                                                    <rect x="992" y="496" width="816" height="32" rx="8" fill="#0284c7" opacity="0.30" />
                                                    <rect x="992" y="496" width="4" height="32" rx="2" fill={COLOR_CYAN} />
                                                </g>
                                            )
                                        } else {
                                            fframes::svgr!(<g></g>)
                                        }
                                    }
                                    <text x="1010" y="518" font-family={FONT} font-size="19" font-weight={if l6_active { "800" } else { "400" }} fill={if l6_active { COLOR_CYAN } else { CODE_PLAIN }}>
                                        "++size_;"
                                    </text>
                                    <text x="1180" y="518" font-family={FONT} font-size="15" fill={TEXT_DIM}>
                                        "// постумова: розмір + 1"
                                    </text>
                                </g>
                            )
                        }
                    </g>

                    // ----- тіло dequeue -----
                    <g opacity={format!("{:.2}", a_deq)}>
                        <text x="1010" y="318" font-family={FONT} font-size="19" font-weight={if active_line == 104 { "800" } else { "400" }} fill={if active_line == 104 { COLOR_EMERALD } else { CODE_PLAIN }}>
                            "void dequeue()"
                        </text>
                        <text x="1010" y="358" font-family={FONT} font-size="19" fill={CODE_PLAIN}>
                            "if (isEmpty())"
                        </text>
                        <text x="1044" y="398" font-family={FONT} font-size="19" fill={CODE_PLAIN}>
                            "throw std::out_of_range(\"Queue underflow\");"
                        </text>
                        {
                            if active_line == 104 {
                                fframes::svgr!(
                                    <g>
                                        <rect x="992" y="416" width="816" height="32" rx="8" fill="#065f46" opacity="0.35" />
                                        <rect x="992" y="416" width="4" height="32" rx="2" fill={COLOR_EMERALD} />
                                    </g>
                                )
                            } else {
                                fframes::svgr!(<g></g>)
                            }
                        }
                        <text x="1010" y="438" font-family={FONT} font-size="19" font-weight={if active_line == 104 { "800" } else { "400" }} fill={if active_line == 104 { COLOR_EMERALD } else { CODE_PLAIN }}>
                            "front_ = (front_ + 1) % capacity_;"
                        </text>
                        {
                            if active_line == 105 {
                                fframes::svgr!(
                                    <g>
                                        <rect x="992" y="456" width="816" height="32" rx="8" fill="#065f46" opacity="0.35" />
                                        <rect x="992" y="456" width="4" height="32" rx="2" fill={COLOR_EMERALD} />
                                    </g>
                                )
                            } else {
                                fframes::svgr!(<g></g>)
                            }
                        }
                        <text x="1010" y="478" font-family={FONT} font-size="19" font-weight={if active_line == 105 { "800" } else { "400" }} fill={if active_line == 105 { COLOR_EMERALD } else { CODE_PLAIN }}>
                            "--size_;"
                        </text>
                        <text x="1010" y="518" font-family={FONT} font-size="15" fill={TEXT_DIM}>
                            "// елемент покидає чергу, слот лишається для rear_"
                        </text>
                    </g>

                    // ----- банер винятку -----
                    {
                        if t >= 12.75 {
                            let ba = ease_out_cubic(clamp((t - 12.75) / 0.35, 0.0, 1.0));
                            fframes::svgr!(
                                <g opacity={format!("{:.2}", ba)} transform={format!("translate(0 {:.1})", (1.0 - ba) * 16.0)}>
                                    <rect x="992" y="548" width="816" height="66" rx="12" fill={COLOR_ROSE} fill-opacity="0.10" stroke={COLOR_ROSE} stroke-width="1.8" />
                                    <rect x="1016" y="566" width="30" height="30" rx="8" fill={COLOR_ROSE} fill-opacity="0.18" />
                                    <text x="1031" y="588" font-family={FONT} font-size="20" font-weight="800" fill={COLOR_ROSE} text-anchor="middle">
                                        "!"
                                    </text>
                                    <text x="1062" y="576" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_ROSE}>
                                        "throw std::overflow_error"
                                    </text>
                                    <text x="1062" y="600" font-family={FONT} font-size="13" fill={TEXT_MUTED}>
                                        "\"Queue overflow: cannot enqueue to full queue\""
                                    </text>
                                </g>
                            )
                        } else {
                            fframes::svgr!(<g></g>)
                        }
                    }
                </g>

                // ================= ПАНЕЛЬ СТАНУ =================
                <g opacity={g_alpha}>
                    <rect x="970" y="660" width="860" height="240" rx="18" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <rect x="992" y="680" width="240" height="30" rx="8" fill="#1e293b" />
                    <text x="1010" y="701" font-family={FONT} font-size="13" font-weight="700" fill={COLOR_INDIGO} letter-spacing="1.2">
                        "СТАН ОБ'ЄКТА"
                    </text>
                    <text x="1806" y="701" font-family={FONT} font-size="14" fill={TEXT_MUTED} text-anchor="end">
                        "Queue q(6)"
                    </text>

                    // front_
                    <rect x="992" y="730" width="254" height="108" rx="12" fill="#0b1226" stroke="#1e293b" stroke-width="1.2" />
                    <text x="1012" y="760" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_EMERALD}>
                        "front_"
                    </text>
                    <text x="1012" y="808" font-family={FONT} font-size="42" font-weight="800" fill={TEXT_MAIN}>
                        { format!("{}", front_display) }
                    </text>
                    <text x="1234" y="808" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="end">
                        "перший на вихід"
                    </text>

                    // rear_
                    <rect x="1270" y="730" width="254" height="108" rx="12" fill="#0b1226" stroke="#1e293b" stroke-width="1.2" />
                    <text x="1290" y="760" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_AMBER}>
                        "rear_"
                    </text>
                    <text x="1290" y="808" font-family={FONT} font-size="42" font-weight="800" fill={TEXT_MAIN}>
                        { format!("{}", rear_display) }
                    </text>
                    <text x="1512" y="808" font-family={FONT} font-size="13" fill={TEXT_DIM} text-anchor="end">
                        "останній доданий"
                    </text>

                    // size_
                    <rect x="1548" y="730" width="260" height="108" rx="12" fill="#0b1226" stroke="#1e293b" stroke-width="1.2" />
                    <text x="1568" y="760" font-family={FONT} font-size="15" font-weight="700" fill={COLOR_CYAN}>
                        "size_"
                    </text>
                    <text x="1568" y="808" font-family={FONT} font-size="42" font-weight="800" fill={TEXT_MAIN}>
                        { format!("{} / 6", count) }
                    </text>
                    {
                        // міні-бар заповнення: 6 комірок (розгорнуто статично)
                        let bar_x: [f32; 6] = [1568.0, 1606.0, 1644.0, 1682.0, 1720.0, 1758.0];
                        let bar_fill: [&str; 6] = [
                            if count >= 1 { COLOR_CYAN } else { "#1e293b" },
                            if count >= 2 { COLOR_CYAN } else { "#1e293b" },
                            if count >= 3 { COLOR_CYAN } else { "#1e293b" },
                            if count >= 4 { COLOR_CYAN } else { "#1e293b" },
                            if count >= 5 { COLOR_CYAN } else { "#1e293b" },
                            if count >= 6 { COLOR_CYAN } else { "#1e293b" },
                        ];
                        fframes::svgr!(
                            <g>
                                <rect x={bar_x[0] as f32} y="816" width="30" height="8" rx="4" fill={bar_fill[0]} />
                                <rect x={bar_x[1] as f32} y="816" width="30" height="8" rx="4" fill={bar_fill[1]} />
                                <rect x={bar_x[2] as f32} y="816" width="30" height="8" rx="4" fill={bar_fill[2]} />
                                <rect x={bar_x[3] as f32} y="816" width="30" height="8" rx="4" fill={bar_fill[3]} />
                                <rect x={bar_x[4] as f32} y="816" width="30" height="8" rx="4" fill={bar_fill[4]} />
                                <rect x={bar_x[5] as f32} y="816" width="30" height="8" rx="4" fill={bar_fill[5]} />
                            </g>
                        )
                    }

                    <text x="992" y="878" font-family={FONT} font-size="14" fill={TEXT_MUTED}>
                        { if full { "isFull() = true -> наступний enqueue кинує std::overflow_error" } else { "isFull() = false -> enqueue коректний: є вільні слоти" } }
                    </text>
                </g>

                // ================= ПАНЕЛЬ ФАЗ =================
                <g opacity={g_alpha}>
                    <rect x="190" y="938" width="1540" height="124" rx="16" fill={CARD_BG} stroke={CARD_BORDER} stroke-width="1.5" />
                    <g transform={format!("translate(230 {})", 1010)}>
                        // таби фаз
                        <rect x="0" y="0" width="284" height="32" rx="8" fill={if phase == 1 { "#334155" } else { "#1e293b" }} />
                        <text x="142" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if phase == 1 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "1. Порожня черга"
                        </text>
                        <rect x="296" y="0" width="284" height="32" rx="8" fill={if phase == 2 { "#0369a1" } else { "#1e293b" }} />
                        <text x="438" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if phase == 2 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "2. enqueue x3 (виробник)"
                        </text>
                        <rect x="592" y="0" width="284" height="32" rx="8" fill={if phase == 3 { "#065f46" } else { "#1e293b" }} />
                        <text x="734" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if phase == 3 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "3. dequeue x2 (споживач)"
                        </text>
                        <rect x="888" y="0" width="284" height="32" rx="8" fill={if phase == 4 { "#92400e" } else { "#1e293b" }} />
                        <text x="1030" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if phase == 4 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "4. wrap-around + fill"
                        </text>
                        <rect x="1184" y="0" width="284" height="32" rx="8" fill={if phase == 5 { "#9f1239" } else { "#1e293b" }} />
                        <text x="1326" y="21" font-family={FONT} font-size="13" font-weight="700" fill={if phase == 5 { TEXT_MAIN } else { TEXT_DIM }} text-anchor="middle">
                            "5. overflow guard"
                        </text>
                    </g>
                    <text x="230" y="968" font-family={FONT} font-size="17" font-weight="700" fill={phase_accent}>
                        { phase_title }
                    </text>
                    <text x="230" y="994" font-family={FONT} font-size="15" fill={TEXT_MUTED}>
                        { phase_desc }
                    </text>
                    <text x="1690" y="968" font-family={FONT} font-size="14" font-weight="700" fill={TEXT_DIM} text-anchor="end">
                        { format!("Час: {:.1}s / 14.0s • кадр {}", t, frame.index) }
                    </text>
                </g>
            </svg>
        )
    }
}
