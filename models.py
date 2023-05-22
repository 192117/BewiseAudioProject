import io

from fastapi import UploadFile
from pydantic import BaseModel, validator
from pydub import AudioSegment


class PeopleRequest(BaseModel):
    """Model for describing the body of the request for the url /user/ ."""

    username: str


class PeopleResponse(BaseModel):
    """Model for describing the description of the response of the objects of the People table."""

    id: int
    user_uuid_token: str


class AudioRequest(BaseModel):
    """Model for describing the body of the request for the url /upload_audio/ ."""

    user_id: int
    user_uuid_token: str
    audio_file: UploadFile

    @validator('audio_file')
    def check_format(cls, audio):
        """Checks that the file has WAV format."""

        content_type = audio.read()
        if not content_type.endswith(b'WAVEfmt '):
            raise ValueError('Invalid audio file format')
        audio.seek(0)
        return audio

    def to_mp3(self):
        """Converts an audio file to MP3 format."""

        audio = AudioSegment.from_file(self.audio_file.file, format='wav')
        mp3_audio = io.BytesIO()
        audio.export(mp3_audio, format='mp3')
        self.audio_file = UploadFile(mp3_audio, filename=f'{self.audio_file.filename.split(".")[0]}.mp3')


class AudioResponse(BaseModel):
    """Model for describing the description of the response of the objects of the Audio table."""

    url: str
