# Веб-сервис для аудиоконвертации

_Это веб-сервис, реализованный на Python 3 с использованием FastAPI и PostgreSQL, выполняющий следующие функции, как 
создание пользователя, для каждого пользователя - преобразование аудиозаписи из формата wav в формат mp3 и запись в 
базу данных и предоставление ссылки для скачивания аудиозаписи._

## Установка

Перед началом установки убедитесь, что у вас установлен Python 3.11 и Poetry (пакетный менеджер для Python). 

Также Вам необходимо установить **ffmpeg**. [Инструкции](https://firstvds.ru/technology/ustanovka-ffmpeg)

1. Склонируйте репозиторий:

`git clone https://github.com/192117/BewiseAudioProject.git`

2. Перейдите в директорию:

`cd BewiseAudioProject`

## Запуск приложения без Docker Compose (после пункта "Установка")

1. Установите зависимости с помощью Poetry:

`poetry install`

2. Создайте переменные окружения:

_Создайте файл .env на основе .env.example для запуска без Docker и файл .env.docker на основе .env.docker.example для 
запуска с Docker. Оба файла содержат переменные окружения, которые требуются для настройки приложения._

3. Запустите приложеие с помощью Poetry:

`poetry run uvicorn app:app --host 0.0.0.0 --port 8000`

4. Доступ к приложению: 

[Документация FastAPI](http://127.0.0.1:8000/docs)

## Запуск приложения c использованием Docker Compose (после пункта "Установка")

1. Создайте переменные окружения:

_Создайте файл .env на основе .env.example для запуска без Docker и файл .env.docker на основе .env.docker.example для 
запуска с Docker. Оба файла содержат переменные окружения, которые требуются для настройки приложения._

3. Запустите сборку docker-compose:

`docker compose up -d --build`

4. Доступ к приложению: 

[Документация FastAPI](http://127.0.0.1:8000/docs)

## Примеры запроса к BewiseProject API

### Создание пользователя

Отправьте POST запрос на http://localhost:8000/user/ с телом запроса в формате JSON следующего вида:

```
{
  "username": "example"
}
```

В случае прохождения валиадции данных получите ответ с uuid_token и id пользователя и **статус код 201**.

_Пример ответа:_

```
{
  "id": 0,
  "user_uuid_token": "string"
}
```

В случае неудачной валидации получите **статус код 422** и сообщение с такой структурой:

```
{
  "error": "string"
}
```

### Загрузка аудиофайла

Отправьте POST запрос на http://localhost:8000/upload_audio/ с телом запроса в формате  multipart/form-data:

```
"user_id"
"user_uuid_token"
"audio_file"
```

В случае прохождения валиадции данных получите ответ с _url_ для скачиванию файла и **статус код 201**.

_Пример ответа:_

```
{
  "url": "string"
}
```

В случае неудачной валидации получите **статус код 422** и сообщение с такой структурой:

```
{
  "error": "string"
}
```

### Скачивание аудиофайла

Отправьте GET запрос на http://localhost:8000/record с параметрами:

```
"id"
"user"
```

В случае прохождения валиадции данных получите начнется загрузка файла.

В случае неудачной валидации получите **статус код 422** и сообщение с такой структурой:

```
{
  "error": "string"
}
```


