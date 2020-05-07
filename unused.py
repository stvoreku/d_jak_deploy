### OLD METHODS
with open('json_data', 'w') as file:
    try:
        data = json.load(file.read)
    except:
        data = []
USER_NUM = len(data)


def get_tracks():
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    c = conn.cursor()
    cmd = "SELECT * FROM tracks ORDER BY TrackID"
    c.execute(cmd)
    res = c.fetchall()
    return res

def get_composer_tracks(name):
    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    cmd = "SELECT Name FROM tracks WHERE Composer = ? ORDER BY Name"
    c.execute(cmd, (name, ))
    res_raw = c.fetchall()
    res = [i for sub in res_raw for i in sub]
    return res
@app.get('/tracks/composers')
def comps(composer_name: str = None):
    res = get_composer_tracks(composer_name)
    if len(res) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No Composer with given Name"})
    return res


@app.get('/tracks')
def tracks(page: int = 0, per_page: int = 10):
    res = get_tracks()
    #if len(res) < (page+1) * per_page:
        #raise HTTPException(status_code=404)
    return res[page*per_page:page*per_page+per_page]


class Album(BaseModel):
    title: str
    artist_id: str


@app.post('/albums', status_code=201)
def post_albums(album: Album):
    res = add_album(album.artist_id, album.title)
    return res

@app.get('/albums/{pk}')
def get_albums(pk: int, compo):
    return get_album(pk)

class Patient(BaseModel):
    name: str
    surname: str


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