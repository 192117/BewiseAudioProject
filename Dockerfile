FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
RUN apt-get update \
    && apt-get install -y ffmpeg
COPY .. .