from urllib.parse import urljoin

import fastapi.openapi.utils as fu
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import Response

from create_db import Audio, connect_db, start_db
from models import AudioResponse, PeopleRequest, PeopleResponse
from utils import handle_file_upload, save_audio, save_user

app = FastAPI(title='BewiseAudioProject API', description='This web service allows users to create an account, '
                                                          'convert their audio recordings from wav to mp3 format, '
                                                          'store them in a database, and provide a download link for '
                                                          'each recording.')


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation exception."""
    return JSONResponse(
        status_code=400,
        content={'error': 'Данные не прошли валидацию!'},
    )


fu.validation_error_response_definition = {
    'title': 'HTTPValidationError',
    'type': 'object',
    'properties': {
        'error': {'title': 'Message', 'type': 'string'},
    },
}


@app.on_event('startup')
async def startup_event():
    start_db()


@app.on_event('shutdown')
async def shutdown_event():
    connect_db().close()


@app.post('/user/', response_model=PeopleResponse, name='add_user')
async def add_user(us: PeopleRequest, db: Session = Depends(connect_db)):
    try:
        data = us.dict()
        user = save_user(data['username'], db)
        return JSONResponse(content=user.json(), status_code=201)
    except IntegrityError as exception:
        raise HTTPException(status_code=400, detail=str(exception.args[0]))


@app.post('/upload_audio/', response_model=AudioResponse, name='add_audio')
async def add_audio(request: Request, user_id: int, user_uuid_token: str, audio_file: UploadFile = File(...),
                    db: Session = Depends(connect_db)):
    try:
        audio_mp3 = await handle_file_upload(audio_file)
        audio, user = save_audio(user_id, user_uuid_token, audio_mp3, db)
        url = request.url_for('record')
        url_response = urljoin(str(url), f'?id={audio.id}&user={user.id}')
        return JSONResponse(content=url_response, status_code=201)
    except IntegrityError as exception:
        raise HTTPException(status_code=400, detail=str(exception.args[0]))


@app.get('/record', name='record')
async def record(id: int, user: int, db: Session = Depends(connect_db)):
    audio = db.query(Audio).filter(Audio.id == id, Audio.people_id == user).first()
    if not audio:
        raise HTTPException(status_code=404, detail='Audio not found')
    response = Response(content=audio.audio_file)
    response.headers['Content-Disposition'] = f'attachment; filename={audio.audio_uuid_identifier}.mp3'
    response.headers['Content-Type'] = 'audio/mp3'
    return response
