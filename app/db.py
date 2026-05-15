from functools import wraps

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def transactional(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            raise e
    return wrapper
