from fastapi import FastAPI, Response, Cookie, HTTPException
from starlette.responses import RedirectResponse
import json
from hashlib import sha256
from basicauth import encode, decode
from pydantic import BaseModel

USER_HASH = "Basic bG9naW46cGFzc3dvcmQ=" "#TB Stored in DB
class Patient(BaseModel):
    name: str
    surename: str

app = FastAPI()

with open('json_data', 'w') as file:
    try:
        data = json.load(file.read)
    except:
        data = []
USER_NUM = len(data)

@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get('/patient')
def get_all():
    return(data)


@app.get('/patient/{pk}')
async def method_get(pk: int):
    try:
        patient = data[pk]
    except IndexError:
        raise HTTPException(status_code=204, detail="Content not found")
    return patient

@app.post('/patient')
async def method_post(patient: Patient):
    temp_num = len(data)
    data.append({'name': patient.name, 'surename': patient.surename})
    USER_NUM = len(data)
    return {"id":temp_num, "patient": {"name":patient.name, "surename":patient.surename}}

@app.get('/welcome')
def welcome():
    return {'msg':'wilkomenn'}

@app.post('/login/')
def login(user: str, password: str, response: Response):
    if decode(USER_HASH) == encode(user, password):
        session_token = sha256(bytes(f"{USER_HASH}{app.secret_key}")).hexdigest()
        response.set_cookie(key="session_token", value=session_token)
        return RedirectResponse('/welcome')
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
