import io
import mimetypes

from fastapi import File, HTTPException, UploadFile
from pydub import AudioSegment
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from create_db import Audio, People


def save_user(username: str, session: Session) -> People:
    """Save People in database.
    :param username: Username of user.
    :param session: Session for working with the database
    :return: People object
    """

    try:
        user = People(username=username)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise


def save_audio(user_id: int, user_uuid_token: str, audio_file: bytes, session: Session) -> (Audio, People):
    """Saves audio data into the database and associates it with a user.
    :param user_id: The ID of the user associated with the audio file.
    :param user_uuid_token: The UUID token of that user.
    :param audio_file: The audio file in bytes format.
    :param session: Session for working with the database
    :return: A tuple containing Audio and People objects.
    """

    try:
        user = session.query(People).filter_by(id=user_id, user_uuid_token=user_uuid_token).first()
        audio = Audio(people_id=user.id, audio_file=audio_file)
        session.add(audio)
        session.commit()
        session.refresh(audio)
        return (audio, user)
    except IntegrityError:
        session.rollback()
        raise


async def handle_file_upload(file: UploadFile) -> File:
    """Converts an audio file uploaded in WAV format to MP3
    :param file: An audio file in the WAV format
    :return: Converted MP3 audio file in bytes
    """

    file_type, _ = mimetypes.guess_type(file.filename)
    if file_type not in ('audio/wav', 'audio/x-wav'):
        return HTTPException(status_code=406, detail='Invalid audio file format (only .wav)')
    audio = AudioSegment.from_file(io.BytesIO(file.file.read()), format='wav')
    mp3_file_bytes = io.BytesIO()
    audio.export(mp3_file_bytes, format='mp3')
    return mp3_file_bytes.getvalue()
