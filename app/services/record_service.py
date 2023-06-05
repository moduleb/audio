import uuid

from flask import abort

from app.dao.models import Audio, User
from app.dao.record_dao import RecordDAO
from app.converter import convert_wav_to_mp3


class RecordService:
    def __init__(self, dao: RecordDAO):
        self.dao = dao

    def save_audio(self, file, user: User) -> Audio:
        """ 1. Получает WAV файл
            2. Извлекает имя файла
            3. Конвертирует в MP3
            4. Создает объект Audio
            5. Сохраняет в базу данных
            6. Возвращает объект Audio  """

        # filename = secure_filename(file.filename)
        audio_uuid = uuid.uuid4()
        filename = audio_uuid
        mp3_file_path = convert_wav_to_mp3(file, filename)

        new_audio = Audio(
            uuid=audio_uuid,
            path=mp3_file_path,
            user_id=user.id
        )

        self.dao.save_audio(new_audio)
        return new_audio

    def get_one_by_uuid(self, uuid: str) -> Audio:
        """Получаем объект Audio из базы данных по uuid"""

        audio_obj = self.dao.get_one_by_uuid(uuid)

        if audio_obj:
            return audio_obj
        else:
            abort(404, f"Аудио с таки uuid не существует")
