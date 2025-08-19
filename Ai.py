import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
import os
import sys
from plyer import notification
import pyautogui
import pywhatkit

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0) 


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
            content = r.recognize_google(audio, language='en-in')
            print("You said: " + content)
            return content.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        except sr.UnknownValueError:
            print("Sorry, I did not understand.")
        except sr.RequestError:
            print("Could not request results.")
    return ""


def get_device_type():
    try:
        result = os.popen('adb devices').read()
        if 'device' in result.split('\n')[1:]:
            return 'android'
    except:
        pass
    return 'desktop'

android_packages = {
    "whatsapp": "com.whatsapp",
    "youtube": "com.google.android.youtube",
    "chrome": "com.android.chrome",
    "instagram": "com.instagram.android",
    "facebook": "com.facebook.katana",
}

contacts = {
    "ck": "+917022970246",
    "naruto": "+917483715788",
    "brightu": "+919019430934",
    "Asif": "+919972146138",
    "sahil": "+916360658897"
}

def open_app(query, device):
    query = query.strip().lower()
    if device == 'desktop':
        pyautogui.press("super")
        pyautogui.write(query)
        pyautogui.sleep(1)
        pyautogui.press("enter")
    elif device == 'android':
        package = android_packages.get(query, query)
        os.system(f'adb shell monkey -p {package} -c android.intent.category.LAUNCHER 1')

def close_app(query, device):
    query = query.strip().lower()
    if device == 'desktop':
        os.system(f'taskkill /f /im {query}.exe')
    elif device == 'android':
        package = android_packages.get(query, query)
        os.system(f'adb shell am force-stop {package}')

def main_process():
    device_type = get_device_type()

    while True:
        request = command().lower()
        if "hello" in request or "hello naruto" in request:
            speak("Hello Asif, How can I help you")


        elif "play song" in request or "play music" in request:
            speak("playing song for you")
            songs = [
                "https://www.youtube.com/watch?v=9ufjVcnpSbo&list=RD9ufjVcnpSbo&start_radio=1",
                "https://www.youtube.com/watch?v=p6ca7gq5H70&list=RDp6ca7gq5H70&start_radio=1",
                "https://www.youtube.com/watch?v=gRRMSF0nB0c&list=RDp6ca7gq5H70&index=2",
                "https://www.youtube.com/watch?v=uK7Ovgs44Uk&list=RDp6ca7gq5H70&index=12",
                "https://www.youtube.com/watch?v=0fB0gr_M7Pw&list=RD0fB0gr_M7Pw&start_radio=1",
                "https://www.youtube.com/watch?v=39-c74jzEMg&list=RD0fB0gr_M7Pw&index=8",
                "https://www.youtube.com/watch?v=NW6Dgax2d6I&list=RD0fB0gr_M7Pw&index=13",
                "https://www.youtube.com/watch?v=VxpOh7_oVr0&list=RD0fB0gr_M7Pw&index=20",
                "https://www.youtube.com/watch?v=k2UYfKL7C2Y&list=RD0fB0gr_M7Pw&index=14",
                "https://www.youtube.com/watch?v=gRRMSF0nB0c&list=RD0fB0gr_M7Pw&index=28"
            ]
            webbrowser.open(random.choice(songs))


        elif "what's time now" in request:
            time = datetime.datetime.now().strftime("%H:%M")
            speak("current time is " + str(time))


        elif "today's date" in request:
            da = datetime.datetime.now().strftime("%d:%m")
            speak("today's date is  " + str(da))


        elif "new task" in request:
            task = request.replace("new task", "").strip()
            if task != "":
                speak("Adding task: " + task)
                with open("list.txt", "a") as file:
                    file.write(task + "\n")

        elif "today's work" in request:
            with open("list.txt", "r") as file:
                speak("today's work is:" + file.read())

        elif "show today's work" in request:
            with open("list.txt", "r") as file:
                tasks = file.read()
                notification.notify(
                    title="Today's work",
                    message=tasks
                )

        elif "open" in request:
            query = request.replace("open", "").strip()
            speak(f"opening {query}")
            open_app(query, device_type)


        elif "close" in request:
            query = request.replace("close", "").strip()
            speak(f"Closing {query}")
            close_app(query, device_type)

            
        elif "screenshot" in request:
            screenshot = pyautogui.screenshot()
            speak("Taking a screenshot")
            screenshot.save("screenshot.png")

        
        elif "what is your name" in request:
            speak("My name is nova , I am your personal assistant")


        elif "stop current task" in request:
            if device_type == 'desktop':
                pyautogui.hotkey('ctrl', 'c')
            elif device_type == 'android':
                os.system('adb shell input keyevent 3')
            else:
                speak("I can't stop..")


        elif "search on google" in request:
            query = request.replace("search on google ", "")
            webbrowser.open("https://www.google.com/search?q=" + query)


        elif "send message to" in request:
            speak("To whom do you want to send the message?")
            name = command().lower()
            if name in contacts:
                speak("What is the message?")
                msg = command()
                speak("Do you want to send it now or schedule it?")
                when = command().lower()
                if "now" in when or "instant" in when:
                    try:
                        pywhatkit.sendwhatmsg_instantly(contacts[name], msg, wait_time=10, tab_close=True)
                        speak("Message sent instantly.")
                    except Exception as e:
                        print("Error:", e)
                        speak("Failed to send the message instantly.")
                elif "schedule" in when or "later" in when:
                    speak("At what hour?")
                    hour = command()
                    speak("And minutes?")
                    minute = command()
                    try:
                        hour = int(hour)
                        minute = int(minute)
                        pywhatkit.sendwhatmsg(contacts[name], msg, hour, minute)
                        speak(f"Message scheduled for {hour}:{minute}.")
                    except:
                        speak("Couldn't understand the time.")
                else:
                    speak("I didn't understand if you wanted to send it now or later.")
            else:
                speak("Sorry, I couldn't find that contact.")

            
        elif "exit" in request or "stop" in request or "bye" in request:
            speak("bye Asif.. , take care..")
            break

def wake_word_listener():
    while True:
        print("Listening for wake word 'Hello Nova'...")
        query = command().lower()
        if "hello nova" in query:
            speak("Hello Asif, how can I help you?")
            main_process()

if __name__ == "__main__":
    if "--autostart" in sys.argv:
        wake_word_listener()
    else:
        speak("Hello Asif, I am ready.")
        main_process()
