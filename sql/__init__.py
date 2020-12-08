from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from bot import DB_URI


engine = create_engine(DB_URI)
BASE = declarative_base()
BASE.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()


class Chats(BASE):
    __tablename__ = "chats"
    chat_id = Column(String(30), primary_key=True)
    chat_title = Column(String(100))

    def __init__(self, chat_id: int, chat_title):
        self.chat_id = str(chat_id)
        self.chat_title = str(chat_title)


class Users(BASE):
    __tablename__ = "users"
    user_id = Column(String(30), primary_key=True)
    username = Column(String(100))
    scores = Column(String(100))

    def __init__(self, user_id: int, username, scores: int):
        self.user_id = str(user_id)
        self.username = str(username)
        self.scores = str(scores)


BASE.metadata.create_all(engine)


def add_chat(chat_id: int, chat_title) -> bool:
    try:
        queryr = session.query(Chats).filter_by(chat_id=str(chat_id)).first()

        if not bool(queryr):
            session.add(Chats(chat_id, chat_title))
            session.commit()
            return True
        else:
            queryr.chat_title = chat_title
            session.commit()
            return True
        return False
    except:
        session.rollback()
        raise
    return False


def get_chats() -> str:
    try:
        queryr = session.query(Chats).all()

        result = ""

        for chat in queryr:
            result += f'{chat.chat_title} - ({chat.chat_id})' + "\n"

        file = open("chatlist.txt", "w", encoding="UTF-8")
        file.write(result)
        file.close()

        return "chatlist.txt"
    except:
        session.rollback()
        raise
    return False


def add_score(chat_id: int, user_id: int, username) -> bool:
    try:
        queryr = session.query(Users).filter_by(user_id=str(user_id)).first()

        if not bool(queryr):
            session.add(Users(user_id, username, 1))
            session.commit()
        else:
            queryr.username = username
            queryr.scores = str(int(queryr.scores) + 1)
            session.commit()
    except:
        session.rollback()
        raise
    return False


def get_scores(user_id: int) -> int:
    try:
        queryr = session.query(Users).filter_by(user_id=str(user_id)).first()

        if not bool(queryr):
            return 0
        else:
            return int(queryr.scores)
    except:
        session.rollback()
        raise
    return False
