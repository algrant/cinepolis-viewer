

import os, sys

# # switch to virtual env, if we're not already there
# INTERP = os.path.expanduser("~/env/cinepolisAPI/bin/python")
# if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

import urllib2
import json
import re
from bs4 import BeautifulSoup
from unidecode import unidecode

# Detailed explanation at http://hitesh.in/2011/running-a-bottle-py-app-on-dreamhost/
#1. Add current directory to path, if isn't already 
cmd_folder = os.path.dirname(os.path.abspath(__file__))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import bottle
from bottle import route, run, template, static_file


#2. Define needed routes here   
@route('/')
def index():
    req = urllib2.urlopen("http://www.cinepolis.com/_CARTELERA/cartelera.aspx?ic=31") #Monterrey = 31, DF = 13

    content = req.read()
    encoding=req.headers['content-type'].split('charset=')[-1]
    soup = BeautifulSoup(unicode(content, encoding))
    
    all_data = {}

    theatres = {}
    movies = {}

    cT_hash = None
    cM_hash = None
    currentTheatre = None
    currentMovie = None

    monterrey_cinepolis = []
    images_to_movieTitles = {}
    titles_to_images = {}

    tags_used = []

    images = []

    movie_endings = ["Esp", "Sub", "Dig", "3D", "4DX", "IMAX", "XE"]

    def parseMovie(m):
        g = m.split(" ")
        i = 0
        title = ""
        tags = []
        while len(movie_endings) > i and (g[-(i+1)] in movie_endings):
            i+=1
        if i > 0:
            return " ".join(g[0:-i]), g[-i:]
        else:
            return m, []

    for tag in soup.recursiveChildGenerator():
        try:
            if tag.name == "span":
                if 'class' in tag.attrs and ("TitulosBlanco" in tag['class']   ):
                    currentTheatre = unicode(tag.string)
                    cT_hash = re.sub('[^0-9a-zA-Z]+', '_', unidecode(currentTheatre))
                    theatres[currentTheatre] = cT_hash
            if tag.name == "a":
                if 'class' in tag.attrs and  "peliculaCartelera" in tag['class'] :
                    currentMovie = unicode(tag.string)
                    cM_hash = re.sub('[^0-9a-zA-Z]+', '_', unidecode(currentMovie))

                    title, tags = parseMovie(currentMovie)
                    title_hash = re.sub('[^0-9a-zA-Z]+', '_', unidecode(title))

                    for t in tags:
                        if t not in tags_used:
                            tags_used.append(t)

                    if title not in movies:
                        movies[title] = title_hash

                    if currentMovie not in all_data:
                        all_data[currentMovie] = {"title":title, "title_hash":title_hash, "hash":cM_hash, "tags":tags, "theatres":{}}

                if 'class' in tag.attrs and  "horariosCarteleraUnderline" in tag['class'] :
                    time = unicode(tag.string);
                    time_href = unicode(tag['href'])

                    if currentTheatre not in all_data[currentMovie]["theatres"]:
                        all_data[currentMovie]["theatres"][currentTheatre] = {"times":[{"time":time, "link":time_href}]}
                    else:
                        all_data[currentMovie]["theatres"][currentTheatre]["times"].append({"time":time, "link":time_href})

            if tag.name =="img":
                image_url = unicode(tag['src']);
                if "http://www.cinepolis.com.mx/Imagenes/Peliculas" in image_url:
                    if "image" not in all_data[currentMovie]:
                        all_data[currentMovie]["image"] = image_url

        except:
            pass

    return template('cinepolis', theatres=theatres, movies=movies, tags=tags_used, data=all_data)

@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static/')

#3. setup dreamhost passenger hook
def application(environ, start_response):
    return bottle.default_app().wsgi(environ,start_response)    

#4. Main method for local developement  
if __name__ == "__main__":
    bottle.debug(True)
    run(reloader=True, port=8020)
