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
    return {'msg':SESSION_TOKEN}

@app.post('/login')
def login(user: str, password: str, response: Response):
    if decode(USER_HASH) == encode(user, password):
        #SESSION_TOKEN = sha256(bytes(f"{USER_HASH}{app.secret_key}")).hexdigest()
        #response.set_cookie(key="SESSION_TOKEN", value=SESSION_TOKEN)
        return RedirectResponse('/welcome')
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
