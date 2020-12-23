from sqlalchemy import Column, String

from sql import BASE, SESSION


class Scores(BASE):
    __tablename__ = "scores"
    user_id = Column(String(30), primary_key=True)
    username = Column(String(100))
    scores = Column(String(100))

    def __init__(self, user_id: int, username, scores: int):
        self.user_id = str(user_id)
        self.username = str(username)
        self.scores = str(scores)


Scores.__table__.create(checkfirst=True)


def add_score(chat_id: int, user_id: int, username) -> bool:
    try:
        queryr = SESSION.query(Scores).filter_by(user_id=str(user_id)).first()

        if not bool(queryr):
            SESSION.add(Scores(user_id, username, 1))
            SESSION.commit()
        else:
            queryr.username = username
            queryr.scores = str(int(queryr.scores) + 1)
            SESSION.commit()
    except:
        SESSION.rollback()
        raise
    return False


def get_scores(user_id: int) -> int:
    try:
        queryr = SESSION.query(Scores).filter_by(user_id=str(user_id)).first()

        if not bool(queryr):
            return 0
        else:
            return int(queryr.scores)
    except:
        SESSION.rollback()
        raise
    return False


def all_scores():
    try:
        return SESSION.query(Scores).all()
    finally:
        SESSION.close()
