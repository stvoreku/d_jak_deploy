from fastapi import FastAPI, Response, Cookie, HTTPException,Depends, status
from starlette.responses import RedirectResponse
from hashlib import sha256
from pydantic import BaseModel
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
USER_HASH = "Basic dHJ1ZG5ZOlBhQzEzTnQ=" #TB Stored in DB
SESSION_TOKEN = ''

app = FastAPI()
app.secret_key = 'dlugi tajny klucz wszedl na plot i mruga'
security = HTTPBasic()
app.session = ''
@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def welcome(session_token: str = Cookie(None)):
    print('welcome, checking session', session_token, 'spodziewany:', app.session)
    if session_token == app.session:
        return "helol"
    raise HTTPException(status_code=401, detail="Unauthorized")


def get_login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_token = 'supertajnytoken'
    print(session_token)
    return session_token


@app.post('/login')
def login(session_token: str = Depends(get_login)):
    response = RedirectResponse(url='/welcome')
    response.status_code = status.HTTP_302_FOUND
    app.session = session_token
    response.set_cookie(key="session_token", value=session_token)
    return response
