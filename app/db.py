from functools import wraps

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def transactional(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
    return wrapper
