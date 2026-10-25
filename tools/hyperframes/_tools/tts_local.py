import re, sys, torch, soundfile as sf
from unicodedata import normalize
from huggingface_hub import hf_hub_download
from ipa_uk import ipa
from styletts2_inference.models import StyleTTS2
from ukrainian_word_stress import Stressifier, StressSymbol
voice = sys.argv[1]; outdir = sys.argv[2]; lines = sys.argv[3:]
stressify = Stressifier()
dev = "cpu"
model = StyleTTS2(hf_path="patriotyk/styletts2_ukrainian_multispeaker", device=dev)
style = torch.load(hf_hub_download("patriotyk/styletts2-ukrainian", f"voices/{voice}.pt", repo_type="space"))
for i, text in enumerate(lines, 1):
    wavs = []
    for t in re.split(r"(?<=[.?!:]) ", text):
        t = t.strip().replace('"', "")
        if not t: continue
        t = normalize("NFKC", t.replace("+", StressSymbol.CombiningAcuteAccent))
        t = re.sub(r"[᠆‐‑‒–—―⁻₋−⸺⸻]", "-", t)
        if t[-1] not in ".?!:-": t += "."
        t = re.sub(r" - ", ": ", t)
        ps = ipa(stressify(t))
        wavs.append(model(model.tokenizer.encode(ps), speed=1.12, s_prev=style))
    w = torch.concatenate(wavs).cpu().numpy()
    sf.write(f"{outdir}/l{i}.wav", w, 24000); print(i, len(w)/24000)
