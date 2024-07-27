![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-black?style=for-the-badge&logo=sqlalchemy&logoColor=red)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

# Flask веб-сервис для конвертации аудио

Основные функции приложения:
- Выдача токена доступа при регистрации пользователя.
- Загрузка WAV аудиозаписей, конвертация в MP3 и дальнейшее сохранение в базе данных.
- Выдача ссылки на скачивание аудиозаписи при предъявлении токена.
- Скачивание файла с сервера

Технологии и инструменты, используемые в приложении:
- Сохранение информации в базе данных Postgres.
- Использование SQLAlchemy для доступа к базе данных.
- Конвертирование аудиофайлов посредством ffmpeg. 
- Разворачивание приложения с помощью Docker Compose.
- Использование Docker Volume для хранения данных Postgres. Доступ к базе открыт для других приложений.


## Запуск приложения:
Для запуска этого Flask веб-сервиса вам потребуется [установить Docker](https://www.docker.com/).

### На локальной машине:

1. Клонировать проект с [Github](https://github.com/ModuleB/audio).
2. Перейти в папку проекта.
3. Запустить приложение Docker.
4. Создать образ:  
`docker compose build`
5. Запустить контейнер:  
`docker compose up -d`
6. Остановить контейнер:  
`docker compose stop`

### На удаленном сервере:
1. Создаем папку для приложения:  
`mkdir audio`
2. Переходим в эту папку:  
`cd audio`
3. Скачиваем файл **'docker-compose.yml'**:   
`wget -O docker-compose.yaml https://raw.githubusercontent.com/ModuleB/audio/master/docker-compose.yaml`
4. Скачиваем файл **'Dockerfile'**:   
`wget -O Dockerfile https://raw.githubusercontent.com/ModuleB/audio/master/Dockerfile`
5. Скачиваем docker образы:  
`docker compose pull`
6. Запустить контейнер:  
`docker compose up -d`
7. Остановить контейнер:  
`docker compose stop`


Приложение доступно по адресу:
- на локальной машине http://0.0.0.0/:8010
- на удаленном сервере http://<IP адрес сервера>:8010


## API Endpoints

Точки доступа API веб-сервиса следующие:

### 1. Создание пользователя

```
POST /users
```

#### Запрос

Тип запроса: form-data

| Параметр | Тип     | Описание                           |
| -------- | ------- |------------------------------------|
| username | string  | Имя пользователя для регистрации.  |

#### Ответ

```json
{
    "uuid": "d75cd4fa-7b77-4645-bb2b-20a3fe6db4b5",
    "token": "8ff9fc43-368f-42f5-98f6-8a3c66e838ca"
}
```
  
  

### 2. Загрузка аудиозаписи
Ожидает наличия токена в заголовке 'Authorization'
```
POST /record
```

#### Запрос

Тип запроса: form-data

| Параметр | Тип | Описание                            |
| -------- |-----| ----------------------------------- |
| file     | WAV | Файл, который необходимо загрузить. |

#### Ответ

```json
{
    "download_url": "http://localhost:5000/record?id=22c8b047-894f-4b03-a7b9-2e4901ad1d1a&user=d75cd4fa-7b77-4645-bb2b-20a3fe6db4b5"
}
```



### 3. Скачивание аудиозаписи

```
GET /record
```

#### Запрос

`http://localhost:5000/record?id=22c8b047-894f-4b03-a7b9-2e4901ad1d1a&user=d75cd4fa-7b77-4645-bb2b-20a3fe6db4b5`

#### Ответ

Ответом будет MP3-аудиофайл


## База данных доступна вне приложения. 
Параметры подключения:

| Параметр  | Значение       |
| --------- | -------------- |
| user      | audio          |
| password  | audio          |
| name      | audio          |
| port      | 5433           |

Для локальной машины используйте следующий адрес хоста: `127.0.0.1`.

Для удаленного сервера используйте IP-адрес сервера в качестве хоста.

