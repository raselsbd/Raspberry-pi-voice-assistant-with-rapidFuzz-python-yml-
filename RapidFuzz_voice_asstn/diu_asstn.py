#!/usr/bin/env python3
import json, time, yaml
import pyttsx3, pyaudio
from vosk import Model, KaldiRecognizer
from rapidfuzz import fuzz
import os

# =============================
# Config
# =============================
VOSK_MODEL_DIR = "/home/rasel/vosk-model-small-en-us-0.15"
YAML_QA_PATH = "qna.yml"
READY_MESSAGE = "I am ready."
SCORE_THRESHOLD = 70  # semantic similarity threshold
MIC_DEVICE_INDEX = 2  # USB Mic index (check with pyaudio loop if needed)

# =============================
# TTS
# =============================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

voices = engine.getProperty("voices")
if voices:
    try:
        eng_voice = next(v for v in voices if "english" in v.id.lower())
        engine.setProperty("voice", eng_voice.id)
    except StopIteration:
        engine.setProperty("voice", voices[0].id)

def speak(text):
    print("Bot:", text)
    os.system(f'espeak-ng "{text}"')  # goes to card0 (Pi jack)

# =============================
# Load YAML QA
# =============================
def load_yaml_qa(path):
    with open(path, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f)
    kb = []
    for section in ["faqs", "smalltalk"]:
        for item in y.get(section, []):
            kb.append((item["q"].strip().lower(), item["a"].strip()))
    return kb

KB = load_yaml_qa(YAML_QA_PATH)

# =============================
# Semantic Match
# =============================
def get_answer(user_input, kb=KB, threshold=SCORE_THRESHOLD):
    user_input = user_input.lower()
    best_match = ("", "", 0)
    for q, a in kb:
        score = fuzz.token_set_ratio(user_input, q)
        if score > best_match[2]:
            best_match = (q, a, score)
    if best_match[2] >= threshold:
        return best_match[1]
    return "Sorry, I did not understand. Please try again."

# =============================
# Vosk STT
# =============================
print("Loading Vosk model...")
vosk_model = Model(VOSK_MODEL_DIR)
rec = KaldiRecognizer(vosk_model, 16000)

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    input_device_index=MIC_DEVICE_INDEX,  # USB mic (card2)
    frames_per_buffer=8000
)
stream.start_stream()

# =============================
# Startup Message
# =============================
time.sleep(0.5)
speak(READY_MESSAGE)
print("Assistant is listening... (say 'exit' or 'bye' to quit)")

# =============================
# Main Loop
# =============================
while True:
    data = stream.read(4000, exception_on_overflow=False)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        user_text = result.get("text", "").strip()
        if not user_text:
            continue

        print("You:", user_text)

        if any(w in user_text.lower() for w in ("exit", "quit", "bye")):
            speak("Goodbye!")
            break

        reply = get_answer(user_text)
        speak(reply)
