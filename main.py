from fastapi import FastAPI, Response, Cookie, HTTPException,Depends
from starlette.responses import RedirectResponse
from hashlib import sha256
from basicauth import encode, decode
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
USER_HASH = "Basic dHJ1ZG5ZOlBhQzEzTnQ=" #TB Stored in DB
SESSION_TOKEN = ''

app = FastAPI()
app.secret_key = 'dlugi tajny klucz wszedl na plot i mruga'
security = HTTPBasic()
app.users = {"trudnY": "PaC13Nt",
@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def welcome(SESSION_TOKEN: str = Cookie(None)):
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.post('/login')
def login(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}
