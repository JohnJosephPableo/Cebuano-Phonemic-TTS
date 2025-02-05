import librosa
import numpy as np
import soundfile as sf

def detect_leading_silence(y, sr, threshold=-100.0):
    """
    Detect leading silence in an audio waveform.
    """
    energy = librosa.feature.rms(y=y)[0]
    threshold = librosa.db_to_power(threshold)
    non_silent_indices = np.where(energy > threshold)[0]
    return non_silent_indices[0] if non_silent_indices.size > 0 else 0

def generate_audio(sybs):
    sounds = []
    sr = 22050  # Default sample rate

    for syb in sybs:
        if syb == ",":
            sound = np.zeros(int(sr * 0.25))  # 250 ms silence
        elif syb == ".":
            sound = np.zeros(int(sr * 0.5))  # 500 ms silence
        else:
            sound, sr = librosa.load(f"test_data/{syb}.wav", sr=sr)
        sounds.append(sound)

    trimmed_sounds = []
    for i, sound in enumerate(sounds):
        if len(sound) > 0:
            start_trim = detect_leading_silence(sound, sr) if i > 0 else 0
            end_trim = detect_leading_silence(sound[::-1], sr) if i < len(sounds) else 0
            trimmed_sound = sound[start_trim: len(sound) - end_trim]
            trimmed_sounds.append(trimmed_sound)

    concatenated_sound = np.concatenate(trimmed_sounds)
    return concatenated_sound, sr

# sybs = ["ka2", "qan0"]
sybs = ["wa0", "laq1", "ra0", "ka0", "qa2", "yu0", "miy1", "rub0", "li2", "ma0", "ni0", "qi2", "ni0"]
output_audio, sr = generate_audio(sybs)

# Save and play
sf.write("output.wav", output_audio, sr)
