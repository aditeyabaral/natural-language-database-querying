import speech_recognition as sr
from googletrans import Translator
from moviepy.editor import VideoFileClip

def audio_to_text(epoch = 1):
    r = sr.Recognizer()
    m = sr.Microphone()
    value, translated = None, None
    with m as source: r.adjust_for_ambient_noise(source, duration = 2)
    print("Recording...")
    with m as source: audio = r.listen(source, timeout = 5)
    while epoch>0:
        try:
            value = r.recognize_google(audio, show_all = False) #fr-FR, hi-IN, kn-IN, ta-IN
            translated = translate(value)
        except sr.UnknownValueError:
            print("Didn't catch that!")
        epoch-= 1
    return value, translated

def video_to_text(filename):
    video = VideoFileClip(filename)
    audio_obj = video.audio
    short_filename = filename[max(0,filename.rfind("/"))+1:filename.rfind(".")]
    audio_obj.write_audiofile(r"Database/Audio/{}.wav".format(short_filename))
    r = sr.Recognizer()
    audiofile = sr.AudioFile(r"Database/Audio/{}.wav".format(short_filename))
    
    with audiofile as source:
        r.adjust_for_ambient_noise(source, duration = 2)

    try:    
        with audiofile as source:
            dur = source.DURATION
            if dur>=180:
                audio = []
                mins = (dur/60)
                offset = 0
                while mins>=0:
                    audio.append(r.record(source, duration = 60, offset = offset))
                    offset = -1
                    mins-=1
            else:
                audio = [r.record(source, duration = source.DURATION)]
                
        transcript = [r.recognize_google(i, show_all = False) for i in audio]
        transcript = " ".join(transcript)
        translated = translate(transcript)
        return transcript, translated
    except UnknownValueError:
        return None

def translate(query):
    translator = Translator()
    source_details = translator.detect(query)
    print(source_details)
    if source_details.lang != "en":
        query = translator.translate(query, src = source_details.lang, dest = "en")
        return query.text 
    else:
        return query


#value, translated = audio_to_text()
#transcript, translated = video_to_text(r"../Database/Video/sample11.mp4")