from fastapi import FastAPI, Response, Cookie, HTTPException,Depends, status, Request
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


class Patient(BaseModel):
    name: str
    surname: str


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get('/welcome')
def welcome(request: Request, session_token: str = Cookie(None)):
    print('welcome, checking session', session_token, 'spodziewany:', app.sessions)
    if session_token in app.sessions.keys():
        return templates.TemplateResponse("welcomen.html", {"request": request, "user": app.sessions[session_token]})
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
    session_token = sha256(bytes(f"{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    print('token created: ', session_token)
    app.sessions[session_token] = credentials.username
    return session_token

def check_session(token):
    if token in app.sessions.keys():
        return app.sessions[token]
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post('/login')
def login(session_token: str = Depends(get_login)):
    response = RedirectResponse(url='/welcome')
    response.status_code = status.HTTP_302_FOUND
    response.set_cookie(key="session_token", value=session_token)
    return response

@app.post('/logout')
def logout(session_token: str = Cookie(None)):
    check_session(session_token)
    del app.sessions[session_token]
    response = RedirectResponse(url='/')
    response.status_code = status.HTTP_302_FOUND
    response.set_cookie(key="session_token", value='')
    return response

### OLD METHODS
with open('json_data', 'w') as file:
    try:
        data = json.load(file.read)
    except:
        data = []
USER_NUM = len(data)


@app.get('/patient')
def get_all(session_token: str = Cookie(None)):
    check_session(session_token)
    return data




@app.get('/patient/{pk}')
async def method_get(pk: int, session_token: str = Cookie(None)):
    check_session(session_token)
    print("asked for {}, currently {}".format(pk, len(data)))
    try:
        patient = data[pk]
    except IndexError:
        raise HTTPException(status_code=204, detail="Content not found")
    return patient

@app.post('/patient')
async def method_post(patient: Patient):
    temp_num = len(data)
    print("DODAJE", patient, "JAKO", len(data))
    data.append({'name': patient.name, 'surname': patient.surname})
    response = RedirectResponse(url='/patient/{}'.format(temp_num))
    USER_NUM = len(data)
    response.status_code = status.HTTP_302_FOUND
    return response
@app.delete('/patient/{pk}')
def delete_patient(pk: int, session_token: str = Cookie(None)):
    check_session(session_token)
    try:
        print("Trying deletion")
        print(data[pk])
        del data[pk]
    except IndexError:
        raise HTTPException(status_code=200, detail="Deleted earlier")
    return "success"