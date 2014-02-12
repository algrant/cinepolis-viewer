#switch to virtual env, if we're not already there

import sys, os

INTERP = os.path.expanduser("~/env/cinepolisAPI/bin/python")
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

import urllib2
import json
from bs4 import BeautifulSoup
#install html5lib, otherwise might fail!

req = urllib2.urlopen("http://www.cinepolis.com/_CARTELERA/cartelera.aspx?ic=31") #Monterrey = 31, DF = 13

content = req.read()
encoding=req.headers['content-type'].split('charset=')[-1]
soup = BeautifulSoup(unicode(content, encoding))
# a = open("cinepolis.html","wb")
# a.write(soup.prettify("utf-8"))

# soup = BeautifulSoup(open("cinepolis.html"))

theatres = []
movies = []


currentTheatre = None
currentMovie = None

monterrey_cinepolis = []
images_to_movieTitles = {}

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
                theatres.append(currentTheatre)
                print currentTheatre.encode('utf8')
        if tag.name == "a":
            if 'class' in tag.attrs and  "peliculaCartelera" in tag['class'] :
                currentMovie = unicode(tag.string)

                title, tags = parseMovie(currentMovie)
                print title.encode('utf8'), tags

                for t in tags:
                    if t not in tags_used:
                        tags_used.append(t)

                if title not in movies:
                    movies.append(title)

                print "\t", currentMovie.encode('utf8')
            if 'class' in tag.attrs and  "horariosCarteleraUnderline" in tag['class'] :
                time = unicode(tag.string);
                time_href = unicode(tag['href'])
                monterrey_cinepolis.append({ "currentMovie": currentMovie, "title": title, "tags": tags, "theatre":currentTheatre, "time": time, "cineLink": time_href})
                print "\t", "\t", time, time_href
        if tag.name =="img":
            image_url = unicode(tag['src']);
            if "http://www.cinepolis.com.mx/Imagenes/Peliculas" in image_url:

                imdat = {"title":title, "img_src":image_url}
                if imdat not in images:
                    images.append(imdat)

                if image_url not in images_to_movieTitles:
                    images_to_movieTitles[image_url] = [title]
                else:
                    if title not in images_to_movieTitles[image_url]:
                        images_to_movieTitles[image_url].append(title)

    except:
        pass

print movies.sort()





print "YES"

a = open("jsondump.json","wb")

movieDATA = {"theatres":theatres, "movies":movies, "images":images, "tags":tags_used, "data":monterrey_cinepolis}


a.write( json.dumps(movieDATA,indent=True, ensure_ascii=True, encoding="utf8"))
