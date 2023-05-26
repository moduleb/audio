from flask import abort

from app.dao.models import Audio


class RecordDAO:
    def __init__(self, session):
        self.session = session


    def save_audio(self, new_audio: Audio) -> None:
        try:
            self.session.add(new_audio)
            self.session.commit()
        except Exception:
            abort(500, "Ошибка базы данных")


    def get_one_by_uuid(self, uuid: str) -> Audio:
        try:
            return self.session.query(Audio).filter(Audio.uuid == uuid).first()
        except Exception:
            abort(500, "Ошибка базы данных")