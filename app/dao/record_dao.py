from app.dao.models import Audio


class RecordDAO:
    def __init__(self, session):
        self.session = session

    def save_audio(self, new_audio: Audio) -> None:
        self.session.add(new_audio)
        self.session.commit()