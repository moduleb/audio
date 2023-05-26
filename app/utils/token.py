import jwt

from app.config import config

SECRET = '$5hfu8Re'
ALGO = 'HS256'

def generate_token(data: dict) -> str:
    """ Функция генерации токена """
    return jwt.encode(data, SECRET, algorithm=ALGO)


def check_token(token: str) -> bool:
    """ Функция проверки токена """
    try:
        jwt.decode(token, SECRET, algorithms=[ALGO])
        return True
    except Exception:
        return False
