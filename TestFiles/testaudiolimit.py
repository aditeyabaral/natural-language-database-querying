import speech_recognition as sr
from moviepy.editor import VideoFileClip

filename = r"Database/Video/sample11.mp4"

video = VideoFileClip(filename)
audio_obj = video.audio
short_filename = filename[max(0,filename.rfind("/"))+1:filename.rfind(".")]
audio_obj.write_audiofile(r"Database/Audio/{}.wav".format(short_filename))
r = sr.Recognizer()
audiofile = sr.AudioFile(r"Database/Audio/{}.wav".format(short_filename))

with audiofile as source:
        r.adjust_for_ambient_noise(source, duration = 2)
        
i = 180
while True:
    print(i)
    with audiofile as source:
        print("Getting audio")
        audio = r.record(source, duration = i)
    print("Got audio")
    try:
        transcript = r.recognize_google(audio, show_all = False)
    except:
        print("Finished!")
        break
    i+=1