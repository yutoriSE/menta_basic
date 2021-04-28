import eel
import desktop
import search

app_name = 'html'
end_point = "index_bs.html"
size = (500, 700)


@ eel.expose
def kimetsu_search(word, csv, dir):
    search.kimetsu_search(word, csv, dir)


desktop.start(app_name, end_point, size)
