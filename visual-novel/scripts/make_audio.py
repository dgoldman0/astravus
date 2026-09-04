#!/usr/bin/env python3
"""Rebuild the chapter's original, deterministic audio (requires NumPy)."""
from pathlib import Path
import wave
import numpy as np

RATE = 24000
OUT = Path(__file__).resolve().parents[1] / 'game' / 'audio'
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(1047)


def save(name, signal, peak):
    signal = signal / max(float(np.max(np.abs(signal))), 1e-9) * peak
    samples = (np.clip(signal, -1, 1) * 32767).astype('<i2')
    with wave.open(str(OUT / name), 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(samples.tobytes())


def fade(signal, seconds=0.15):
    n = int(RATE * seconds)
    signal[:n] *= np.linspace(0, 1, n)
    signal[-n:] *= np.linspace(1, 0, n)
    return signal


def note(freq, length, pluck=False):
    t = np.arange(int(length * RATE)) / RATE
    body = np.sin(2 * np.pi * freq * t)
    body += .18 * np.sin(2 * np.pi * freq * 2 * t)
    body += .045 * np.sin(2 * np.pi * freq * 3 * t)
    if pluck:
        env = (1 - np.exp(-t * 50)) * np.exp(-t * 1.4)
    else:
        env = np.sin(np.pi * t / length) ** 2
    return body * env

# Four slow suspended harmonies; a sparse, recurring five-note motif.
score = np.zeros(48 * RATE)
chords = [(130.81, 196, 293.66), (110, 164.81, 261.63),
          (87.31, 174.61, 261.63), (98, 196, 293.66)]
for i, chord in enumerate(chords):
    for freq in chord:
        voice = note(freq, 12)
        score[i * 12 * RATE:(i + 1) * 12 * RATE] += .16 * voice
for i, freq in enumerate([523.25, 587.33, 659.25, 392, 523.25, 440, 392, 523.25]):
    start = int((3 + i * 5) * RATE)
    voice = note(freq, 4, True)
    score[start:start + len(voice)] += .20 * voice
save('first_light.wav', fade(score, 1), .33)

# Seamless circular filters avoid a click at the ambience loop boundary.
noise = rng.normal(size=12 * RATE)
air = sum(np.roll(noise, i) for i in range(70)) / 70
water = sum(np.roll(noise, i) for i in range(9)) / 9
save('garden_air.wav', .7 * air + .055 * water, .17)
noise = rng.normal(size=16 * RATE)
rain = sum(np.roll(noise, i) for i in range(5)) / 5
for _ in range(180):
    i = rng.integers(0, len(rain) - 1200)
    t = np.arange(1200) / RATE
    rain[i:i + 1200] += .5 * np.sin(2 * np.pi * rng.uniform(600, 1400) * t) * np.exp(-t * 140)
save('rain.wav', rain, .22)
t = np.arange(int(.6 * RATE)) / RATE
wood = (np.sin(2 * np.pi * 170 * t) + .4 * np.sin(2 * np.pi * 281 * t)) * np.exp(-t * 17)
wood += .08 * rng.normal(size=len(t)) * np.exp(-t * 30)
save('wood.wav', fade(wood, .005), .20)
print('Created four original PCM WAV assets.')
