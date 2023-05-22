import secrets

from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

from configuration import DATABASE_URL

Base = declarative_base()


class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    user_uuid_token = Column(String, unique=True, nullable=False, default=secrets.token_hex(16))
    audios = relationship('Audio', backref='people')

    def json(self):
        return {
            'id': self.id,
            'user_uuid_token': self.user_uuid_token,
        }

    def __repr__(self):
        return f'User: {self.username}, uuid: {self.user_uuid_token}'


class Audio(Base):
    __tablename__ = 'audio'

    id = Column(Integer, primary_key=True)
    audio_file = Column(LargeBinary)
    people_id = Column(Integer, ForeignKey('people.id'))
    audio_uuid_identifier = Column(String, unique=True, nullable=False, default=secrets.token_hex(16))

    def __repr__(self):
        return f'Audio uuid: {self.audio_uuid_identifier}'


def connect_db():
    """Function to connect to database and return session object.
    :return: Session object
    """

    try:
        engine = create_engine(DATABASE_URL, connect_args={})
        session = Session(bind=engine.connect())
        yield session
    finally:
        session.close()


def start_db():
    """Function to start the database
    :return: None
    """

    engine = create_engine(DATABASE_URL, connect_args={})
    session = Session(bind=engine.connect())
    Base.metadata.create_all(bind=engine)
    session.close()
