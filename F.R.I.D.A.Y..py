import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import cv2
import pywhatkit as kit
import sys
import pyautogui
import time
import operator
import requests
from bs4 import BeautifulSoup

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Ready To Comply. What can I do for you Boss!?")

def open_application(app_name):
    app_paths = {
        'genshin impact': r"D:\EPIC GAMES\Genshin Impact\Genshin Impact game\GenshinImpact.exe",
        'waves': r"D:\EPIC GAMES\WutheringWavesj3oFh\launcher.exe",
    }

    app_name_lower = app_name.lower()

    if app_name_lower in app_paths:
        try:
            os.startfile(app_paths[app_name_lower])
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Failed to open {app_name}: {str(e)}")
    else:
        speak(f"App {app_name} not found")

website_urls = {
    'instagram': "https://www.instagram.com/",
    'twitter': "https://twitter.com/",
    'facebook': "https://www.facebook.com/",
    'anime': "https://hianime.to/home",
    # Add more websites as needed
}

def open_website(website_name):
    website_name = website_name.lower()
    if website_name in website_urls:
        webbrowser.open(website_urls[website_name])
        speak(f"Opening {website_name.capitalize()}")
    else:
        speak(f"Sorry, I don't have {website_name} in my list.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        root.after(0, lambda: listening_overlay.lift())
        listening_label.config(text="Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        root.after(0, lambda: listening_overlay.lower())
        listening_label.config(text="")
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        speak("Can you please repeat that again boss...")
        return "None"
    return query

def listenForWakeWord(wake_word="friday"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Listening for wake word...")
            root.after(0, lambda: listening_overlay.lift())
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='en-in').lower()
                if wake_word in query:
                    root.after(0, lambda: listening_overlay.lower())
                    return
            except Exception as e:
                continue

def execute_command():
    while True:
        listenForWakeWord()
        wishMe()
        while True:
            query = takeCommand().lower()

            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'search on youtube' in query:
                speak("What would you like to search on YouTube?")
                search_query = takeCommand().lower()
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

            elif 'open app' in query:
                app_name = query.replace('open app', '').strip()
                open_application(app_name)


            elif 'close opera' in query:
                os.system("taskkill /f /im opera.exe")

            elif 'close youtube' in query:
                os.system("taskkill /f /im msedge.exe")

            elif 'open google' in query:
                speak("What should I search?")
                qry = takeCommand().lower()
                webbrowser.open(f"https://www.google.com/search?q={qry}")


            elif 'open website' in query:
                website_name = query.replace('open website', '').strip()
                open_website(website_name)

            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            elif "shut down the system" in query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in query:
                os.system("shutdown /r /t 5")

            elif "lock the system" in query:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "open command prompt" in query:
                os.system("start cmd")

            elif "close command prompt" in query:
                os.system("taskkill /f /im cmd.exe")

            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()

            elif "take screenshot" in query:
                speak('Tell me a name for the file')
                name = takeCommand().lower()
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("Screenshot saved")

            elif "calculate" in query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Ready")
                    print("Listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)

                def get_operator_fn(op):
                    return {
                        '+': operator.add,
                        '-': operator.sub,
                        'x': operator.mul,
                        'divided': operator.__truediv__,
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)

                speak("Your result is")
                speak(eval_binary_expr(*(my_string.split())))

            elif "volume up" in query:
                for _ in range(15):
                    pyautogui.press("volumeup")

            elif "volume down" in query:
                for _ in range(15):
                    pyautogui.press("volumedown")

            elif "mute" in query:
                pyautogui.press("volumemute")

            elif "who are you" in query or "hu r u" in query:
                speak('My Name Is Friday. I can do everything that my creator programmed me to do.')

            elif "who created you" in query:
                speak("My Boss's name is Pradhumn, and I was created using Python language.")

            elif 'type' in query:
                query = query.replace("type", "")
                pyautogui.write(f"{query}")

            elif "shutdown" in query:
                speak('Alright then, I am switching off')
                root.quit()
                return

# Function to update GIF frames
def update_frame(ind):
    frame = frames[ind]
    ind += 1
    if ind == len(frames):
        ind = 0
    gif_label.config(image=frame)
    root.after(100, update_frame, ind)

def on_press(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def on_drag(event):
    x = root.winfo_pointerx() - x_offset
    y = root.winfo_pointery() - y_offset
    root.geometry(f"+{x}+{y}")

# Setting up the GUI
root = tk.Tk()
root.title("Virtual Assistant GUI")
root.geometry("500x400")
root.overrideredirect(True)  # Remove the title bar

# Configure the root window to have the desired background color
root.configure(bg="#050117", bd=5)

gif_path = r"C:\Users\hp\PycharmProjects\Friday\9c6a8841bca92519d7c8bf1952c0f104.gif"
gif_image = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(gif_image)]

gif_label = tk.Label(root, bg="#050117")
gif_label.pack()

listening_label = tk.Label(root, text="", font=("Helvetica", 16), fg="white", bg="#050117")
listening_label.pack(pady=20)

# Add a label for the listening text overlay
listening_overlay = tk.Label(root, text="Listening...", font=("Helvetica", 12), fg="white", bg="#050117")
listening_overlay.place(relx=0.5, rely=0.9, anchor=tk.CENTER)  # Position at the bottom center
listening_overlay.lower()  # Hide initially

# Bind the events to make the window draggable
root.bind("<Button-1>", on_press)
root.bind("<B1-Motion>", on_drag)

# Start the execution thread for commands
command_thread = threading.Thread(target=execute_command)
command_thread.start()

# Function to update GIF frames
def update_frame(ind):
    frame = frames[ind]
    ind += 1
    if ind == len(frames):
        ind = 0
    gif_label.config(image=frame)
    root.after(100, update_frame, ind)

# Start updating the GIF frames
update_frame(0)

# Run the main event loop
root.mainloop()
