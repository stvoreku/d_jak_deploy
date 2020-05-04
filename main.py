from fastapi import FastAPI, Response, Cookie, HTTPException,Depends, status, Request
import sqlite3
from starlette.responses import RedirectResponse
from hashlib import sha256
from pydantic import BaseModel
import json
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.secret_key = 'dlugi tajny klucz wszedl na plot i mruga'
security = HTTPBasic()
app.sessions = {}


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d






def get_tracks():
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    cmd = "SELECT * FROM tracks ORDER BY TrackID"
    c.execute(cmd)
    res = c.fetchall()
    return res

def get_composer_tracks(name):
    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    cmd = "SELECT Name FROM tracks WHERE Composer = ? ORDER BY Name"
    c.execute(cmd, (name, ))
    res_raw = c.fetchall()
    res = [i for sub in res_raw for i in sub]
    return res

def add_album(artist_id, name):
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    test_cmd = "SELECT COUNT(*) FROM artists WHERE ArtistId = ?"
    c.execute(test_cmd, (artist_id,))
    test_res = c.fetchone()
    print(test_res['COUNT(*)'])
    if test_res['COUNT(*)'] < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No Artist with given id"})
    cmd = "INSERT INTO albums (ArtistId, Title) VALUES (?, ?)"
    c.execute(cmd, (artist_id, name,))

    cmd = "SELECT * FROM albums WHERE Title = ? AND ArtistId = ?"
    c.execute(cmd, (name, artist_id,))
    res = c.fetchone()
    return res
def get_album(pk):
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    cmd = "SELECT * FROM albums WHERE AlbumId = ?"
    c.execute(cmd, (pk, ))
    return c.fetchone()

@app.get('/tracks/composers')
def comps(composer_name: str = None):
    res = get_composer_tracks(composer_name)
    if len(res) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No Composer with given Name"})
    return res


@app.get('/tracks')
def tracks(page: int = 0, per_page: int = 10):
    res = get_tracks()
    #if len(res) < (page+1) * per_page:
        #raise HTTPException(status_code=404)
    return res[page*per_page:page*per_page+per_page]


class Album(BaseModel):
    title: str
    artist_id: str


@app.post('/albums', status_code=201)
def post_albums(album: Album):
    res = add_album(album.artist_id, album.title)
    return res

@app.get('/albums/{pk}')
def get_albums(pk: int):
    return get_album(pk)


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}



print(add_album(21, "hells bells"))