import datetime
import os
import playsound
import random
import subprocess
import speech_recognition as sr
from gtts import gTTS

greet = ["hi", "hello", "howdy", "greetings"]
note_cmd = ["make a note", "write this down", "remember this", "note this"]
del_cmd = ["delete", "remove", "remove file", "delete file"]
cmdlisten = "start"


def speak(txt):
    tts = gTTS(text=txt, lang="en")
    filename = "botspeech.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def get_voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        micinput = r.listen(source)
        speech = r.recognize_google(micinput)
        print(speech)
    return speech


def note(txt, name):
    if name != "default":
        filename = str(name)
    else:
        date = datetime.datetime.now()
        filename = str(date).replace(":", "-") + "-note.txt"
    with open(filename, "w") as f:
        f.write(txt)
    subprocess.Popen(["notepad.exe", filename])

def delete(filename):
    try:
        os.remove(filename)
    except:
        print(f'{filename} could Not deleted')


def del_call(stt):
    for d in del_cmd:
        if d in stt:
            speak("Please name the targeted file for deletion")
            fname = get_voice_input()
            speak(f'You are about to delete {fname}, are you sure?')
            del_perm = get_voice_input()
            if "yes" in del_perm:
                delete(fname)
            else: speak("delete operation aborted")
    

def greet_call(stt):
    for g in greet:
        if g in stt:
            speak(random.choice(greet))

def note_call(stt):
    for phrase in note_cmd:
        if phrase in stt:
            speak("can you tell me the note's content ? ")
            content = get_voice_input()
            speak("would you like to name this file ? else say default")
            fname = get_voice_input()
            note(content, fname)
            speak("Done")


speak("i'm on")
while True:
    stt = get_voice_input()
    greet_call(stt)
    note_call(stt)
    del_call(stt)