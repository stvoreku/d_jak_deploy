from fastapi import FastAPI, Response, Cookie, HTTPException,Depends, status
from starlette.responses import RedirectResponse
from hashlib import sha256
from basicauth import encode, decode
from pydantic import BaseModel
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
USER_HASH = "Basic dHJ1ZG5ZOlBhQzEzTnQ=" #TB Stored in DB
SESSION_TOKEN = 'tajnytoken'

app = FastAPI()
app.secret_key = 'dlugi tajny klucz wszedl na plot i mruga'
security = HTTPBasic()

@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.post('/welcome')
def welcome(session_token: str = Cookie(None)):
    if session_token == SESSION_TOKEN:
        return "helol"
    print(session_token, SESSION_TOKEN)
    raise HTTPException(status_code=401, detail="Unauthorized")


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudny")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post('/login')
def login(credentials: HTTPBasicCredentials = Depends(security)):
    response = RedirectResponse(url='/welcome')
    response.status_code = status.HTTP_307_TEMPORARY_REDIRECT
    response.set_cookie(key="session_token", value=SESSION_TOKEN)
    return response
