from pydub import AudioSegment
# from pydub.playback import play
from pydub.silence import detect_leading_silence
import pytsmod as tsm

def generate_audio(sybs):
    sounds = []
    # Get all syllable audio
    for syb in sybs:
        # sound = AudioSegment.empty()
        # if syb == ",":
        #     sound = AudioSegment.silent(duration=250)
        # elif syb == ".":
        #     sound = AudioSegment.silent(duration=500)
        # else:
        sound = AudioSegment.from_wav("test_data/" + syb + ".wav")
        sounds.append(sound)
    # Trim silence on extremities
    trimmed_sounds = []
    for i in range(len(sounds)):
        start_trim = 0
        end_trim = 0
        if i > 0:
            start_trim = detect_leading_silence(sounds[i], silence_threshold=-55.0)
        if i < len(sounds):
            end_trim = detect_leading_silence(sounds[i].reverse(), silence_threshold=-55.0)
        trimmed_sound = sounds[i][start_trim:len(sounds[i])-end_trim]
        trimmed_sounds.append(trimmed_sound)
    concatenated_sound = AudioSegment.empty()
    for sound in trimmed_sounds:
        concatenated_sound += sound
    concatenated_sound.export("output.wav", format="wav")
    return concatenated_sound
