
import notify2
import dbus
import settings
import speech_recognition as sr
import subprocess

import urllib
from bs4 import BeautifulSoup
import requests
import webbrowser

result = []
def google(text):
    text = urllib.parse.quote_plus(text)
    url = 'https://google.com/search?hl=en&q=' + text
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for g in soup.find_all(class_='g'):
        result.append(g.text)
    return result[1] 


notify2.init('LTU Assistant')

text_only_mode = False

def speak(message, also_cmd=False):
    '''Speak the given message using the text-to-speech backend.'''
    if also_cmd or text_only_mode:
        print(message)
    try:
        notification = notify2.Notification('LTU Assistant',
                                            message,
                                            'notification-message-im')
        notification.show()
    except dbus.exceptions.DBusException:
        if not also_cmd:
            print(message)
    if not text_only_mode:
        if settings.voice == 'female':
            # Speak using a female voice
            subprocess.call('espeak -s 125 -v f4 -p 40 "' + message + '"', shell=True)
        else:
            # Default to male voice
            subprocess.call('espeak -s 125 -v f4 -p 40 "' + message + '"', shell=True)

def listen():
    '''Gets a command from the user, either via the microphone or command line
    if text-only mode was specified.'''
    if text_only_mode:
        ret = raw_input('\t> ')
        return True, ret
    else:
        # obtain audio from the microphone
        r = sr.Recognizer()
        ret = ""
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            # Timeout after 10 seconds, in case this doesn't work
            audio = r.listen(source, 10)

        # recognize speech using Google Speech Recognition
        try:

            print("Sending recorded speech to Google...")
            sentence = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said '" + sentence + "'.")
            speak("Google Speech Recognition thinks you said '" + sentence + "'.")

            print(google(sentence))
            speak(google(sentence))
            return True, sentence
        except sr.UnknownValueError:
            ret = "Google Speech Recognition could not understand audio."
        except sr.RequestError:
            ret = "Could not request results from Google Speech Recognition."
        return False, ret

def ask_question(question, also_cmd=False):
    '''Ask the user a question and return the reply as a string.'''
    speak(question, also_cmd)
    num_tries = 3
    for x in range(0, num_tries):
        (success, sentence) = listen()
        if success:
            return sentence
        else:
            speak('I\'m sorry, could you repeat that?', also_cmd)
    speak('I\'m sorry, I could not understand you.', also_cmd)
    return ''

if __name__ == '__main__':
    (success, error) = listen()
    if not success:
        print(error)
