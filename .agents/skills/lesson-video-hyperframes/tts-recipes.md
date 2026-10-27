# Voice-over recipes

Use only the option the user chose. Every recipe must end with `assets/vo/l1.wav … lN.wav` in the project, loudness-normalised (`ffmpeg -af loudnorm=I=-16:TP=-1.5:LRA=7 -ar 44100 -ac 1`), and a printout of each line's duration and inner pauses (`ffmpeg -i l.wav -af silencedetect=noise=-32dB:d=0.1 -f null -`).

## Local StyleTTS2-ukrainian (used for the CNN module)
- Script: `tools/hyperframes/_tools/tts_local.py "<voice>" <outdir> "<line 1>" "<line 2>" …`; wrapper `_tools/new_video.sh <id> "<line>" …` also creates the project and copies music/SFX.
- Model `patriotyk/styletts2_ukrainian_multispeaker`; voice files `voices/<name>.pt` from the HF Space `patriotyk/styletts2-ukrainian` (the user picked «Вʼячеслав Дудко», apostrophe U+02BC); speed 1.12; CPU is fine.
- Stress is marked with `+` after the vowel ("ев+ал") only for ambiguous words; numbers are spelled out in words.
- The venv is built in the session scratchpad and may be gone. Rebuild: `uv venv --python 3.11 <scratch>/tts-venv && <scratch>/tts-venv/bin/pip install torch==2.8.0 styletts2-inference ukrainian-word-stress ipa-uk soundfile huggingface_hub`, then run with `TTS_PY=<scratch>/tts-venv/bin/python`.
- The public HF Space's ZeroGPU quota runs out for free users; running the model locally avoids it.

## Other options (ask first; none is preinstalled)
- **Hosted TTS** (HeyGen and others): load the `media-use` skill; needs the user's key; the audio is sent to the provider, so confirm first.
- **Other local TTS** (Piper, Kokoro, Coqui…): check that the language and voice licence suit the site before installing anything.
- **User-recorded audio:** ask for one file per line (or one file plus line start times); trim silence, normalise, then continue with step 4.
- **No voice:** on-screen text carries the narration; use longer holds (≥ 2.5 s per idea) and the music bed only.

## Music
`_music/bed-ambient.wav` (MusicGen-small ambient, looped with crossfades) is copied to each project as `assets/music/bed.wav` (volume 0.16, fade-in 1.5 s, fade-out 2 s — `make_index.py` writes this). MusicGen-small is CC BY-NC 4.0: credit «Музика: MusicGen (Meta), CC BY-NC 4.0» on the site if it is used (not yet added). A new bed: generate in the TTS venv, loop with crossfades, `loudnorm` to −18 LUFS.
