import jwt

from app.config import config


def generate_token(data: dict) -> str:
    """ Функция генерации токена """
    return jwt.encode(data, config.SECRET, algorithm=config.ALGO)


def check_token(token: str) -> bool:
    """ Функция проверки токена """
    try:
        jwt.decode(token, config.SECRET, algorithms=[config.ALGO])
        return True
    except Exception:
        return False
