import os
from tkinter import *
import time

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("NLQ")
        self.root.configure(background = '#121212')
        self.root.geometry('800x500')
        self.root.iconbitmap('icon.ico')
        self.vidPath = StringVar()
        self.vidPath.set("")
        self.blank = Label(self.root, bg= '#121212')
        self.blank.pack()
        self.welcome = Label(self.root, text = 'Welcome to QueVideo!',background = '#121212')
        self.welcome.config(fg='#3b54ce',font = ("Comfortaa",40))
        self.welcome.pack()
        self.blank = Label(self.root,bg= '#121212')
        self.blank.pack()
        self.blank = Label(self.root,bg= '#121212')
        self.blank.pack()
        self.content = Message(self.root, textvariable = self.vidPath, bg= '#121212', font = ("Calibri"), fg = "white")
        self.content.pack()
        self.blank = Label(self.root, bg= '#121212')
        self.blank.pack()
        self.search = Button(self.root, text = 'SEARCH', command = self.searchQueryAudio, bg = '#4759b8', fg = 'white', font = ("Comfortaa",15))
        self.search.config(height = 2, width = 30, borderwidth = 0)
        self.search.pack(side = TOP, expand=1)
        self.blank = Label(self.root, bg= '#121212')
        self.blank.pack()
        self.launch = Button(self.root, text = 'PLAY', command = self.launchVideo, bg = '#4759b8', fg = 'white', font = ("Comfortaa",15))
        self.launch.config(height = 2, width = 30, borderwidth = 0)
        self.launch.pack(side = TOP, expand=1)
        self.launch.pack()
        self.blank = Label(self.root, bg= '#121212')
        self.blank.pack()
        self.root.mainloop()

    def searchQueryAudio(self):
        #_, text = speechRecognition.audio_to_text()
        #path = get correct video --return the path
        #self.vidPath.set(path)
        path = r"C:\Users\Aditeya\Desktop\Aditeya\GitHub\Natural-Language-Database-Querying\Database\Video\vid4.mp4"
        self.vidPath.set(path)

        
    def launchVideo(self):
        p = self.vidPath.get()
        if p and p!='No video selected':
            os.system(p)
        else:
            self.vidPath.set("No video selected")
            #time.sleep(1)
App()