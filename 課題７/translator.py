import eel
import os
import desktop
from googletrans import Translator

app_name = os.path.dirname(__file__)+'/html'
end_point = 'index.html'
size = (1200, 800)

translator = Translator()


@ eel.expose
def translate_to_japanese(text):
    eel.view_log_js(translator.translate(text, dest='ja').text)


@ eel.expose
def translate_to_english(text):
    eel.view_log_js(translator.translate(text, dest='en').text)


desktop.start(app_name, end_point, size)
