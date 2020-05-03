### OLD METHODS
with open('json_data', 'w') as file:
    try:
        data = json.load(file.read)
    except:
        data = []
USER_NUM = len(data)


@app.get('/patient')
def get_all(session_token: str = Cookie(None)):
    print("asking for all patients,")
    check_session(session_token)
    jsonized = {}
    for a in range(len(data)):
        jsonized[a] = data[a]
    print(jsonized)
    return jsonized


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
        raise HTTPException(status_code=204, detail="Deleted earlier")
    response = Response()
    response.status_code=status.HTTP_204_NO_CONTENT
    return response