import os
import uuid

from pydub import AudioSegment
from werkzeug.utils import secure_filename

from app.config import config
from app.dao.models import Audio, User
from app.dao.record_dao import RecordDAO


class RecordService:
    def __init__(self, dao: RecordDAO):
        self.dao = dao

    def to_mp3(self, file, user: User) -> Audio:

        # Получаем имя файла
        filename = secure_filename(file.filename)

        # Передаем расположение кодеков
        AudioSegment.converter = f'{os.getcwd()}/app/converter/ffmpeg'
        AudioSegment.ffprobe = f'{os.getcwd()}/app/converter/ffprobe'

        # Загружаем файл как WAV
        wav_file = AudioSegment.from_wav(file)

        # Экспортируем MP3
        mp3_file_path = f"{config.UPLOAD_FOLDER}{filename.rsplit('.', 1)[0].lower()}.mp3"
        wav_file.export(mp3_file_path, format="mp3")

        # Создаем объект Audio
        new_audio = Audio(
            uuid=uuid.uuid4(),
            path=mp3_file_path,
            user_id=user.id
        )

        # Сохраняем
        self.dao.save_audio(new_audio)

        return new_audio
