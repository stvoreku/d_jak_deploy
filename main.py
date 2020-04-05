from fastapi import FastAPI, HTTPException
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
def get_all():
    return(data)


@app.get('/patient/{pk}')
async def method_get(pk: int):
    try:
        patient = data[pk]
    except IndexError:
        raise HTTPException(status_code=204, detail="Content not found")
    return {"name": patient.name, "surename": patient.surename}

@app.post('/patient')
async def method_post(patient: Patient):
    temp_num = len(data)
    data.append({'name': patient.name, 'surename': patient.surename})
    USER_NUM = len(data)
    return {"id":temp_num, "patient": {"name":patient.name, "surename":patient.surename}}