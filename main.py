from fastapi import FastAPI
import json
app = FastAPI()
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    surename: str


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
def method_get():
    return {"data":data}

@app.post('/patient')
async def method_post(patient: Patient):
    data.append({'name': patient.name, 'surename': patient.surename})
    USER_NUM = len(data)
    return {"id":USER_NUM-1, "patient": {"name":patient.name, "surename":patient.surename}}