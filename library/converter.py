import speech_recognition as sr
from gtts import gTTS
from moviepy.video.io import ffmpeg_tools
import PyPDF2
from .models import Book
import pyttsx3

def speech_txt(voice_note, language):
    r = sr.Recognizer()
    voice_note = "." + voice_note
    ffmpeg_tools.ffmpeg_extract_audio(voice_note, 'note.wav')
    sound = './note.wav'
    with sr.AudioFile(sound) as source:
        audio = r.listen(source)
        try:
            my_text = r.recognize_google(audio, language=language)
            results = {
                'my_text': my_text,
                'status':'success'
            }
        except Exception as e:
            results = {
                'status': 'unsuccessful',
                'e':e
            }
        return results

def txt_speech(mytext, language):
    language='en'
    try:
        myaudio = gTTS(text=mytext, lang=language, slow=False)
        return myaudio
    except:
        return "Error"


def book_reader(id):
    book = Book.objects.get(id=id)
    file_dir = '.'+book.book.url
    text=''
    try:
        pdfReader = PyPDF2.PdfFileReader(open(file_dir, 'rb'))
        for page_num in range(pdfReader.numPages):
            text2 = pdfReader.getPage(page_num).extractText()
            text = text+ '' + text2
        engine = pyttsx3.init()
        engine.save_to_file(text, 'static/audio.mp3')
        engine.runAndWait()
        engine.stop()
        #myaudio = gTTS(text=text, lang='en')
        #myaudio.save('audio.mp3')
        results = {
            'status':'success'
        }           

    except Exception as e:
        results = {
            'status': 'unsuccessful',
            'e':e
        }
    return results