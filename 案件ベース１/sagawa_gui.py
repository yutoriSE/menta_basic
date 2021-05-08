import os
import eel
import desktop
import sagawa

app_name = os.path.dirname(__file__)+'/html'
end_point = 'index.html'
size = (500, 180)

s = sagawa.Sagawa()


@eel.expose
def start_scraping(path):
    s.start_scraping(path)


desktop.start(app_name, end_point, size)
