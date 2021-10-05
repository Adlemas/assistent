import speech_recognition as sr
import pyttsx3

from evdev import uinput, ecodes as ec

micro = sr.Microphone()
r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('voice', 'russian')

# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale


def change_voice(eng, language, gender='VoiceGenderFemale'):
    for voice in eng.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            eng.setProperty('voice', voice.id)
            return True

    raise RuntimeError(
        "Language '{}' for gender '{}' not found".format(language, gender))


print(change_voice(engine, b'\x05ru', 'male'))


def talk(x):
    engine.say(x)
    engine.runAndWait()


def listen():
    text = ''
    with micro as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, phrase_time_limit=4)
        try:
            text = (r.recognize_google(audio, language="ru-RU")).lower()
        except(sr.UnknownValueError):
            pass
        except(TypeError):
            pass
    print(text)
    return text


def say(text):
    print(text)
    talk(text)


commands = {
    "скажи": say
}

ignore_words = ['пожалуйста', 'если можешь', 'будь любезен', 'можешь']


def command(msg):
    if msg == '':
        return
    for ignore in ignore_words:
        msg = msg.replace(ignore+' ', '')
    for word in msg.split(' '):
        if word in commands:
            commands[word](msg[len(word)+1:])


def wait():
    text = listen()
    if 'привет' in text:
        talk('здравствуйте сэр. что нужно сделать?')
        cmd = listen()
        while not cmd.startswith('пока'):
            command(cmd)
            cmd = listen()
    talk('досвидания сэр')
    wait()


wait()
