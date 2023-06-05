import os
import platform

from flask import abort
from pydub import AudioSegment

from app.config import config


def set_codec():
    """ Определяем операционную систему и в зависимости от нее указываем путь к кодекам """
    if platform.system() == "Darwin":
        AudioSegment.converter = f'{os.getcwd()}/app/converters/mac/ffmpeg'
        AudioSegment.ffprobe = f'{os.getcwd()}/app/converters/mac/ffprobe'
    elif platform.system() == "Windows":
        AudioSegment.converter = f'{os.getcwd()}/app/converters/windows/ffmpeg.exe'
        AudioSegment.ffprobe = f'{os.getcwd()}/app/converters/windows/ffprobe.exe'
    elif platform.system() == "Linux":
        AudioSegment.converter = f'{os.getcwd()}/app/converters/linux/ffmpeg'
        AudioSegment.ffprobe = f'{os.getcwd()}/app/converters/linux/ffprobe'


def convert_wav_to_mp3(file, filename: str) -> str:
    """Конвертирует полученный файл в MP3,
    возвращает путь до файла"""

    # Устанавливаем кодек
    set_codec()

    try:
        # Загружаем файл как WAV
        wav_file = AudioSegment.from_wav(file)

        # Экспортируем MP3
        # mp3_file_path = f"{config.UPLOAD_FOLDER}{filename.rsplit('.', 1)[0].lower()}.mp3"
        # mp3_file_path = f"{os.path.join(config.UPLOAD_FOLDER)}/{filename}.mp3"

        filename = f"{filename}.mp3"
        mp3_file_path = os.path.join(config.UPLOAD_FOLDER, filename)
        wav_file.export(mp3_file_path, format="mp3")
        return filename

    except FileNotFoundError:
            print("Возможно отсутствует папка 'app/data' для сохранения аудиофайлов")
            abort(500, 'Ошибка декодирования файла')

    except Exception:
            abort(500, 'Ошибка декодирования файла')