import calendar
import datetime

import jwt

from app.config import config


def generate_token(data):
    # days1000 = datetime.datetime.utcnow() + datetime.timedelta(days=1000)
    # data['exp'] = calendar.timegm(days1000.timetuple())
    return jwt.encode(data, config.SECRET, algorithm=config.ALGO)

def check_token(token):
    try:
        jwt.decode(token, config.SECRET, algorithms=[config.ALGO])
        return True
    except Exception:
        return False
