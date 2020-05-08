from fastapi import FastAPI, Response, Cookie, HTTPException,Depends, status, Request
import sqlite3
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


@app.get('/sales')
def sales(category: str):
    res = category
    return res
@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}