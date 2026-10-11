import os
import soundfile as sf
from kokoro_onnx import Kokoro

model_path = os.path.expanduser('~/.cache/hyperframes/tts/models/kokoro-v1.0.onnx')
voices_path = os.path.expanduser('~/.cache/hyperframes/tts/voices/voices-v1.0.bin')

kokoro = Kokoro(model_path, voices_path)

scenes = [
    ("vo_scene1.wav", "Your cycle should not be something you have to guess.", 1.05),
    ("vo_scene2.wav", "Meet Celine. A simpler, mathematically secure way to understand your cycle.", 1.05),
    ("vo_scene3.wav", "Track your cycle phases, basal body temperature, and daily symptoms with effortless ease.", 1.05),
    ("vo_scene4.wav", "Turn raw cycle data into meaningful clinical insights, designed specifically for irregular rhythms, PMDD, and PCOS.", 1.05),
    ("vo_scene5.wav", "Simple. Private. Made for you. With zero-knowledge encryption, your intimate data remains mathematically yours.", 1.05),
    ("vo_scene6.wav", "Know your cycle. Know yourself. Experience menstrual health with complete trust.", 1.05),
    ("vo_scene7.wav", "Start tracking today at celine period tracking dot vercel dot app.", 1.05)
]

out_dir = 'brag-output/composition/assets/audio'
os.makedirs(out_dir, exist_ok=True)

for fname, text, speed in scenes:
    samples, sr = kokoro.create(text, voice="af_heart", speed=speed, lang="en-us")
    out_path = os.path.join(out_dir, fname)
    sf.write(out_path, samples, sr)
    dur = len(samples) / sr
    print(f"Generated {fname}: {dur:.2f}s")
