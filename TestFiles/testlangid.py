from google.cloud import speech_v1p1beta1
import io


def sample_recognize(text):
    """
    Transcribe a short audio file with language detected from a list of possible
    languages

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.flac'

    # The language of the supplied audio. Even though additional languages are
    # provided by alternative_language_codes, a primary language is still required.
    language_code = "en"

    # Specify up to 3 additional languages as possible alternative languages
    # of the supplied audio.
    alternative_language_codes_element = "es"
    alternative_language_codes_element_2 = "en"
    alternative_language_codes = [
        alternative_language_codes_element,
        alternative_language_codes_element_2,
    ]
    config = {
        "language_code": language_code,
        "alternative_language_codes": alternative_language_codes,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # The language_code which was detected as the most likely being spoken in the audio
        print(u"Detected language: {}".format(result.language_code))
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        
text = r"C:/Users/Aditeya/Desktop/Intel NLQ/harvard.wav"
sample_recognize(text)