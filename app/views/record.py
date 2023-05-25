
import uuid
from flask import request, flash, redirect, send_file
from flask_restx import Namespace, Resource
from pydub import AudioSegment
from werkzeug.utils import secure_filename

from app.config import config
from app.container import user_service
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

        # проверим, передается ли в запросе файл
        if 'file' not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю
            flash('Не могу прочитать файл')
            return 'Не могу прочитать файл'
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return 'Нет выбранного файла'
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = secure_filename(file.filename)
            # сохраняем файл
            file.save(f'{config.UPLOAD_FOLDER}{filename}')

            # # Load your WAV file
            wav_file = AudioSegment.from_wav(f'{config.UPLOAD_FOLDER}{filename}')
            #
            # # Export as MP3
            mp3_file = f"{config.UPLOAD_FOLDER}{filename.rsplit('.', 1)[0].lower()}.mp3"
            wav_file.export(mp3_file, format="mp3")


            user = user_service.get_one_by_uuid(request.form["uuid"])
            new_audio = Audio(
                uuid=uuid.uuid4(),
                path=mp3_file,
                user_id=user.id
            )
            db_session.add(new_audio)
            db_session.commit()

            environ = request.environ
            environ = environ.get('HTTP_HOST')
            url = f'http://{environ}/record?id={new_audio.uuid}&user={user.id}'
            return redirect(url)



@record_ns.route("/")
class AudioView(Resource):
    def get(self):
        uuid = request.args.get('id')
        audio_obj = db_session.query(Audio).filter(Audio.uuid == uuid).first()
        audio_path = audio_obj.path
        return send_file(f'.{audio_path}', as_attachment=True)
