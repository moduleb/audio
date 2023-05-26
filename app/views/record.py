from flask import request, redirect, send_file, abort
from flask_restx import Namespace, Resource

from app.container import user_service, record_service

record_ns = Namespace('/record')


@record_ns.route("/upload")
class UploadView(Resource):
    def post(self):
        # Получаем файл из запроса
        file = get_file_from_request(request)

        # Получаем uuid пользователя из запроса
        user_uuid = get_uuid_from_post_request(request)

        # Запрашиваем пользователя у базы данных
        user = user_service.get_one_by_uuid(user_uuid)

        # Сохраняем аудио и получаем объект
        new_audio = record_service.save_audio(file, user)

        # Получаем текущий хост и порт
        environ = request.environ.get('HTTP_HOST')

        # Отдаем ссылку на скачивание файла
        url = f'http://{environ}/record?id={new_audio.uuid}&user={user.uuid}'
        return redirect(url)


@record_ns.route("/")
class AudioView(Resource):
    def get(self):

        uuid = request.args.get('id')

        if not uuid:
            abort(400, "В запросе отсутствует обязательный параметр 'uuid'")

        # Получаем объект Audio из базы данных
        audio_obj = record_service.get_one_by_uuid(uuid)

        try:
            audio_path = audio_obj.path
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

    # Проверяем расширение файла
    if '.' not in file.filename:
        abort(400, "Неопознанный тип файла")

    file_extension = file.filename.rsplit('.', 1)[1].lower()

    # Расширения файлов, которые разрешено загружать
    ALLOWED_EXTENSIONS = ['wav']

    if file_extension not in ALLOWED_EXTENSIONS:
        abort(400, f"Неподдерживаемый тип файла. Разрешены только: {ALLOWED_EXTENSIONS}")

    return file


def get_uuid_from_post_request(request):
    # Получаем uuid пользователя
    user_uuid = request.form.get("uuid")

    if not user_uuid:
        abort(400, "В запросе отсутствует обязательный параметр 'uuid'")

    return user_uuid
