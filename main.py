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

@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def welcome(session_token: str = Cookie(None)):
    print(session_token, SESSION_TOKEN)
    if session_token == SESSION_TOKEN:
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
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}")).hexdigest()
    print(session_token)
    return session_token


@app.post('/login')
def login(session_token: str = Depends(get_login)):
    response = RedirectResponse(url='/welcome')
    response.status_code = status.HTTP_302_FOUND
    SESSION_TOKEN = session_token
    response.set_cookie(key="session_token", value=session_token)
    return response
