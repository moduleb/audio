

from flask import request, redirect, send_file
from flask_restx import Namespace, Resource

from app.container import user_service, record_service
from app.dao.models import Audio
from app.database import db_session


record_ns = Namespace('/record')

# # расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'wav'}


def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@record_ns.route("/upload")
class UploadView(Resource):
    def post(self):

        # Проверим, передается ли в запросе файл
        if 'file' not in request.files:
            return "В запросе отсутствует обязательный параметр 'file'", 400

        # Получаем файл
        file = request.files['file']

        # Если файл пуст... (если файл не выбран, браузер может отправить пустой параметр 'file')
        if file.filename == '' or not file:
            return "Отсутствует файл", 400

        # Получаем uuid пользователя
        user_uuid = request.form.get("uuid")

        if not user_uuid:
            return "В запросе отсутствует обязательный параметр 'uuid'", 400

        if not allowed_file(file.filename):
            return "Неподдерживаемый тип файла. Разрешены только: 'WAV'", 400

        # Запрашиваем пользователя у базы данных
        user = user_service.get_one_by_uuid(user_uuid)

        if not user:
            return "Пользователь не найден", 400

        # Сохраняем аудио и получаем объект
        new_audio = record_service.to_mp3(file, user)

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
            return f"В запросе отсутствует обязательный параметр 'uuid'", 400

        audio_obj = db_session.query(Audio).filter(Audio.uuid == uuid).first()

        if not audio_obj:
            return f"Аудио с таким uuid: '{uuid}' не найдена", 404

        try:
            audio_path = audio_obj.path
            return send_file(f'.{audio_path}', as_attachment=True)
        except Exception as e:
            return f'Ошибка сервера. Аудиофайл не найден', 500
