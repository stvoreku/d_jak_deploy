from fastapi import FastAPI, Response, Cookie, HTTPException
from starlette.responses import RedirectResponse
from hashlib import sha256
from basicauth import encode, decode
from pydantic import BaseModel

USER_HASH = "Basic dHJ1ZG5ZOlBhQzEzTnQ=" #TB Stored in DB
SESSION_TOKEN = ''

app = FastAPI()
app.secret_key = 'dlugi tajny klucz wszedl na plot i mruga'


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def welcome(SESSION_TOKEN: str = Cookie(None)):
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.post('/login')
def login(login: str, password: str, response: Response):
    raise HTTPException(status_code=401, detail="Unauthorized")
