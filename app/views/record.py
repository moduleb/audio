from flask import request, redirect, send_file, abort
from flask_restx import Namespace, Resource

from app.config import config
from app.container import user_service, record_service
from app.utils.token import check_token

record_ns = Namespace('/record')


@record_ns.route("/upload")
class UploadView(Resource):
    def post(self):
        # Получаем файл из запроса
        file = get_file_from_request(request)

        # Получаем token пользователя из запроса
        token = get_token_from_post_request(request)

        # Проверяем token
        if not check_token(token):
            abort(400, "Неверный токен доступа")

        # Получаем uuid пользователя из запроса
        user_uuid = get_uuid_from_post_request(request)

        # Запрашиваем пользователя у базы данных
        user = user_service.get_one_by_uuid(user_uuid)

        if not user:
            abort(404, "Пользователя с таким uuid не существует")

        # Сохраняем аудио и получаем объект
        new_audio = record_service.save_audio(file, user)

        # Получаем текущий хост и порт
        environ = request.environ.get('HTTP_HOST')

        # Отдаем ссылку на скачивание файла
        url = f'http://{environ}/record?id={new_audio.uuid}&user={user.uuid}'

        response = {"download_url": url}

        return response


@record_ns.route("/")
class AudioView(Resource):
    def get(self):

        uuid = request.args.get('id')

        if not uuid:
            abort(400, "В запросе отсутствует обязательный параметр 'id'")

        # Получаем объект Audio из базы данных
        audio_obj = record_service.get_one_by_uuid(uuid)

        # Отправляем файл пользователю
        try:
            audio_path = config.UPLOAD_FOLDER + "/" + audio_obj.path
            return send_file(f'{audio_path}', as_attachment=True)
        except Exception:
            abort(500, 'Ошибка сервера. Аудиофайл не найден')


def get_file_from_request(request):

    # Проверим, передается ли в запросе файл
    if 'file' not in request.files:
        abort(400, "В запросе отсутствует обязательный параметр 'file'")

    # Получаем файл
    file = request.files['file']

    # Если файл пуст... (если файл не выбран, браузер может отправить пустой параметр 'file')
    if file.filename == '' or not file:
        abort(400, "Отсутствует файл")

    # Проверяем, существует ли расширение у файла (есть ли точка в названии)
    if '.' not in file.filename:
        abort(400, "Неопознанный тип файла")

    # Получаем расширение файла
    file_extension = file.filename.rsplit('.', 1)[1].lower()

    # Список расширений файлов, которые разрешено загружать
    ALLOWED_EXTENSIONS = ['wav']

    # Проверяем расширение файла
    if file_extension not in ALLOWED_EXTENSIONS:
        abort(400, f"Неподдерживаемый тип файла. Разрешены только: {ALLOWED_EXTENSIONS}")

    return file


def get_uuid_from_post_request(request):

    # Получаем uuid пользователя
    user_uuid = request.form.get("uuid")

    if not user_uuid:
        abort(400, "В запросе отсутствует обязательный параметр 'uuid' или его значение не задано")

    return user_uuid


def get_token_from_post_request(request):

    # Получаем token из запроса
    token = request.headers("Authorization")

    if not token:
        abort(400, "В запросе отсутствуют данные аутентификации")

    return token
