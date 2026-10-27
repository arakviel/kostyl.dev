---
name: lesson-video-hyperframes
description: Make an explainer/lesson video with HyperFrames (HTML→mp4/webm) for any lesson or article on this site and embed it where the page has a `<!-- VIDEO … -->` slot. Use when the user asks for lesson videos or animations, when new `<!-- VIDEO` slots appear (`grep -rn "^<!-- VIDEO" content`), or when an existing video must be fixed or rebuilt. Works for any subject; the user is asked about voice-over, music and look before building, and approves a preview before anything is published.
---

# Lesson videos with HyperFrames

Read the `hyperframes` skill first for the render contract. This skill is the **repo recipe**: how a slot becomes a finished, embedded video. It is subject-agnostic; the examples in the "Worked example" section come from the CNN module (`content/16.ai-python/15.cnn-image-classification/`).

## Standing rules
- **Ask before building, preview before publishing** (see Workflow steps 1 and 7). Never render for delivery, publish into `public/` or edit a lesson before the user has approved the preview of that video — unless the user explicitly waives the approval for the current batch ("без превʼю"). A waiver applies to that batch only; ask again next time.
- **Never delete or replace existing media** (old `anim-*`, images). New videos are added next to them unless the user says otherwise.
- Embed as `<video controls preload="metadata" playsinline poster=… class="diagram-img rounded-xl shadow-lg w-full my-6">` with mp4 + webm sources and a jpg poster (not GIF). Narrated videos have no autoplay/muted. `_tools/embed.py` writes this.
- Never write a token or other secret into a file.
- Talk to the user in the language they write (so far Ukrainian); on-screen and spoken language follows the lesson.
- Do not commit unless asked. Commit trailer: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.

## Accuracy rules (every subject)
1. Every figure, quote, date, formula or code output on screen comes from the lesson itself, from a primary source, or from re-running the lesson's own code/data. Check that a reproduced value equals what the lesson states before using it; if they differ, stop and tell the user.
2. Illustrations that are invented (toy data, schematic diagrams) are labelled as such or are obviously schematic, and stay consistent with how the real thing behaves.
3. Never interpolate or "smooth" a displayed measurement. Show recorded values only.
4. Facts taken from papers/books/standards are marked as such, the way the lesson does.
5. Keep reproduced data in a small file next to the project (e.g. `_data/*.json`) so the video can be rebuilt.
6. In the final report, separate "real / reproduced", "from sources" and "illustrative" content, and list deviations from the slot spec.

## Questions to ask the user (use AskUserQuestion; skip what the user already decided in this session or in memory)
Ask in one batch before step 3:
- **Voice-over:** none (music + on-screen text only) / local TTS (e.g. StyleTTS2-ukrainian, Piper, Kokoro, Coqui — whatever fits the language) / hosted TTS (via the `media-use` skill, needs a key) / the user records it themselves. If they pick a TTS, ask which voice and whether stress marks are needed (Ukrainian). Do not assume StyleTTS2.
- **Music:** none / a given file / generated (e.g. MusicGen — mention its licence: CC BY-NC means attribution and non-commercial use) / bundled library tracks.
- **Look:** default dark house look or something else (see "Look").
- **Length and depth** when the slot spec is vague (one idea per video, usually 40–70 s).
- **Preview format:** snapshots contact sheet (default) or live Studio preview (`npx hyperframes preview --background`, stop with `--stop`).
Record the answers in the memory file for this workflow so they need not be asked again unless the user wants to change them.

## Layout of this repo
| What | Where |
|---|---|
| project per video | `tools/hyperframes/<module>/<slot-id>/` (`index.html`, `compositions/world.html`, `compositions/lines.html`, `assets/{vo,music,sfx,img}`) |
| helpers | `tools/hyperframes/_tools/`: `new_video.sh`, `make_index.py`, `check.sh`, `publish.sh`, `embed.py`, `sheet.py`, `tts_local.py` |
| music | `tools/hyperframes/_music/` |
| published | `public/videos/<course>/<module>/<lesson-folder>/<name>.{mp4,webm}`, poster `public/images/<…>/<name>-poster.jpg` |
The helpers currently have the CNN module's paths hard-coded (`ROOT`, module folder, `TTS_PY`). For another module copy/parametrise them first (a one-line change per script) and keep the same file layout. `new_video.sh` is TTS-specific; if the user chose another voice option, create the project with `npx hyperframes init <id> --non-interactive` and put audio in `assets/vo/l1.wav…`.

`<lesson-folder>`/`<name>`: if the slot's `file:` line names a path, use it. Otherwise choose a short name in the lesson's image folder. Re-publishing the same name overwrites the files and the embed stays valid.

## Workflow
1. **Find and read the slot.** `grep -rn -A14 "^<!-- VIDEO" content/…`. Read `one-thing`, `example`, `beats`, `on-screen`, `vo`, `look` and the lesson text and code output around it. Spec text is a suggestion; where it conflicts with the lesson (numbers, style), follow the lesson and tell the user. Then **ask the questions above**.
2. **Gather real data** (accuracy rules): lesson text, cached results, the lesson's scripts. Make assets (PNG via PIL; `Image.NEAREST` for pixel art).
3. **Write the narration** (4–6 lines, ~45–65 s). Numbers spelled out in words. Synthesize it with the chosen voice and get each line's **duration and inner pauses** — they place on-screen events on the exact words. (Voice recipes: see the reference file `tts-recipes.md` next to this skill.)
4. **Timeline table** before coding: line → absolute start/end → events. Line 1 starts ~0.4 s, 0.6–0.7 s between lines, total = last line end + ~3 s (closing claim card ~2.6 s).
5. **Compose.** `compositions/world.html` (one `<template>`, `#root` 1920×1080, `window.__timelines["world"]`). Generate data-driven markup in JS (grids, dots); for big data write the file from a script that inlines JSON. `compositions/lines.html` holds the closing claim card. `index.html` via `make_index.py <id> <total> '<VO [[start,dur],…]>' '<SFX [[name,start,dur],…]>'`.
6. **Check.** `_tools/check.sh <id>` must come back empty for lint/runtime/layout/motion/contrast/craft. Fix, don't suppress. Then `npx hyperframes snapshot --at …` and `python3 _tools/sheet.py <project-dir> <scratch>/sheet.png`; Read the sheet and compare positions/values against the data, not just "looks fine".
7. **Preview and approval stop.** Show the user what was built: the snapshot sheet (or Studio link), the narration text with timings, which numbers are real/sourced/illustrative, and ask for approval or changes. Wait. Iterate until approved. (Skip only under an explicit waiver.)
8. **Publish** after approval: `_tools/publish.sh <id> <name> <lesson-folder> <poster-sec>` → renders at delivery quality and prints duration, LUFS and peak; encodes mp4/webm/jpg. Read the poster jpg once.
9. **Embed**: `python3 _tools/embed.py <lesson.md> <slot-id> <lesson-folder> <name>` (accepts `<!-- VIDEO\nid: x` and `<!-- VIDEO id: x`). For a video without a slot first insert a minimal `<!-- VIDEO\nid: <id>\n-->` where it belongs.
10. **Verify**: no `^<!-- VIDEO` left for finished slots; every `src=`/`poster=` in the lesson resolves under `public/`.
11. **Report**: duration, LUFS/peak, content classes (real / sourced / illustrative), deviations from the spec; say plainly that sound was measured, not listened to, unless the user listened. Offer a commit.

## Look (default, change only if the user asks)
1920×1080, 30 fps, background `#070b14`, accents cyan `#22d3ee`, emerald `#34d399`, amber `#fbbf24`, rose `#fb7185`, text `#e8eef7`, muted `#9fb2cf`; Inter + JetBrains Mono; text ≥ 32 px (SVG text ≥ 28 px), big numbers 56–150 px mono; one idea per video; ≤ 90 s.

## Gotchas
- `check` flags **`dead_stretch`** after ~3 s with nothing visibly changing (it ignores SVG attribute changes). Fill gaps with opacity/scale pulses or text changes that match the narration.
- CSS custom properties set via `Object.assign(el.style, {"--c": …})` are ignored — use `style.setProperty` or a real property.
- GSAP tweens on `top`/`left` are errors (`gsap_non_transform_motion`); animate `x/y/scale/opacity/width/height`.
- No `tl.call` for text swaps (use paired elements + opacity). `fromTo` on many targets applies from-values at build time; use paired `to`.
- The same image used twice → `duplicate_media_discovery_risk`; copy it under another name.
- Text over text → `content_overlap` (e.g. claim card vs a header): fade the header first. Text covering a marker/cell needs `data-layout-allow-occlusion="true"` on the covered element.
- Contrast: text on coloured cells switches to light when luminance < ~110; SVG `font-family` needs a fallback ("Inter, sans-serif").
- Grow lines with element width/height or sliced `points`, not `stroke-dashoffset`.
- Overlay windows/markers: derive offsets from the element's CSS left/top and compare with the cells they should cover in a snapshot. Anything meant to appear later starts at `opacity:0` and is revealed by the narrated event.
- First frame is the social thumbnail: have the key image/title visible at t=0 (`tl.set`).
- The CLI adds `data-hf-id` to markup → edit files with Edit/regex, not exact raw `replace`. Always `cd` to an absolute project path per command; in zsh `set -- $x` does not word-split.
- For many points use a beeswarm layout (sort by x, lowest free level); for values that pile up at the ends use a non-linear axis and say so on screen.

## Worked example (CNN module)
35 videos for lessons 01–16 of `15.cnn-image-classification`: data came from `scripts/*_core.py` and `temp/*_cache.pt` (run with the system `python3` from the repo root), narration was generated with local StyleTTS2-ukrainian (voice «Вʼячеслав Дудко»), music was a looped MusicGen ambient bed (`_music/bed-ambient.wav`, volume 0.16, fades 1.5/2 s), finished mixes landed at −13…−15.7 LUFS. Those were built under a "no preview" waiver the user gave for that batch; a new batch needs its own decision.
