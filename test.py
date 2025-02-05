from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import detect_leading_silence
import pytsmod as tsm
import numpy as np
import sounddevice as sd
import soundfile as sf

# sound1 = AudioSegment.from_wav("test_data/ku0.wav")
# # start_trim = detect_leading_silence(sound1, silence_threshold=-55.0)
# end_trim = detect_leading_silence(sound1.reverse(), silence_threshold=-55.0)
# trimmed_sound1 = sound1[:len(sound1)-end_trim]
# sound2 = AudioSegment.from_wav("test_data/an1.wav")
# start_trim = detect_leading_silence(sound2, silence_threshold=-55.0)
# # end_trim = detect_leading_silence(sound2.reverse(), silence_threshold=-55.0)
# trimmed_sound2 = sound2[start_trim:len(sound2)]
# combined_sounds = trimmed_sound1 + trimmed_sound2
# play(combined_sounds)
# combined_sounds.export("test_data/output.wav", format="wav")

def generate_audio(sybs):
    sounds = []
    # Get all syllable audio
    for syb in sybs:
        sound = AudioSegment.empty()
        if syb == ",":
            sound = AudioSegment.silent(duration=250)
        if syb == ".":
            sound = AudioSegment.silent(duration=500)
        else:
            sound = AudioSegment.from_wav("data/speech_database/" + syb + ".wav")
        sounds.append(sound)
    # Trim silence on extremities
    trimmed_sounds = []
    for i in range(len(sounds)):
        start_trim = 0
        end_trim = 0
        if i > 0:
            start_trim = detect_leading_silence(sounds[i], silence_threshold=-35.0)
        if i <= len(sounds):
            end_trim = detect_leading_silence(sounds[i].reverse(), silence_threshold=-35.0)
        trimmed_sound = sounds[i][start_trim:len(sounds[i])-end_trim]
        trimmed_sounds.append(trimmed_sound)
    concatenated_sound = AudioSegment.empty()
    for sound in trimmed_sounds:
        concatenated_sound += sound
    return concatenated_sound

# sybs = ["da2", "qan0"]
sybs = ["wa0", "laq1", "ra0", "ka0", "qa2", "yu0", "miy1", "rub0", "li2", "ma0", "ni0", "qi2", "ni0"]
output = generate_audio(sybs)
play(output)

def pydub_to_np(audio: AudioSegment) -> tuple[np.ndarray, int]:
    """
    Converts pydub audio segment into np.float32 of shape [duration_in_seconds*sample_rate, channels],
    where each value is in range [-1.0, 1.0]. 
    Returns tuple (audio_np_array, sample_rate).
    """
    return np.array(audio.get_array_of_samples(), dtype=np.float32).reshape((-1, audio.channels)) / (
            1 << (8 * audio.sample_width - 1)), audio.frame_rate

new_sound = pydub_to_np(output)[0]
speed_up = tsm.wsola(new_sound, 0.25)
# sd.default.channels = 2
sd.play(speed_up)
sd.wait()
print(output.sample_width)
output.export("output.wav", format="wav")
sf.write("new_output.wav", speed_up, 44000)
