from sqlalchemy import create_engine, Integer, String, Column, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
import os
import pandas

BDPATH = 'botdb.db'

base = declarative_base()
engine = create_engine('sqlite:///botdb.db?check_same_thread=False', echo=False)
session = sessionmaker(bind=engine)()


class Users(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True, nullable=False)
    level = Column(String(20))
    course1 = Column(String(20))
    course2 = Column(String(20))
    test1 = Column(Integer)


class Course(base):
    __tablename__ = 'course'

    id = Column(Integer, primary_key=True)
    level = Column(String, unique=True, nullable=False)
    message = Column(String, unique=True, nullable=False)
    answer = Column(String)
    next_level = Column(String)
    image = Column(String)


if not os.path.exists(BDPATH):
    base.metadata.create_all(engine)

    data = pandas.read_excel('info.xlsx', sheet_name='c', engine='openpyxl')
    levels = data['Level'].tolist()
    messages = data['Message'].tolist()
    answers = data['Answer'].tolist()
    next_levels = data['Next'].tolist()
    images = data['Image'].tolist()

    for i in range(len(levels)):
        session.add(Course(level=levels[i], message=messages[i], answer=answers[i], next_level=next_levels[i],
                           image=images[i]))

    session.commit()


def add_user(chat_id):
    if not has_user(chat_id):
        session.add(Users(chat_id=chat_id))
        session.commit()


def get_user(chat_id):
    user = session.query(Users).filter_by(chat_id=chat_id).one()
    return user


def has_user(chat_id: str) -> bool:
    is_exists = session.query(exists().where(Users.chat_id == str(chat_id))).scalar()
    return is_exists


def get_user_level(chat_id: str) -> str:
    level = session.query(Users.level).filter_by(chat_id=chat_id).one()
    return level[0]


def set_level(chat_id: str, level: str):
    user = session.query(Users).filter_by(chat_id=chat_id).first()
    user.level = level
    session.commit()


def pass_course(chat_id: str, level: str):
    user = session.query(Users).filter_by(chat_id=chat_id).first()
    if level.split('.')[0] == '1':
        user.course1 = "pass"
    if level.split('.')[0] == '2':
        user.course2 = "pass"
    session.commit()


def pass_test1(chat_id: str, mark):
    user = session.query(Users).filter_by(chat_id=chat_id).first()
    user.test1 = mark
    session.commit()


def statistics(chat_id: str):
    user = session.query(Users).filter_by(chat_id=chat_id).first()
    c1 = user.course1
    c2 = user.course2
    t1 = user.test1
    return [c1, c2, t1]


def get_message(level: str) -> str:
    if has_level(level):
        message = session.query(Course.message).filter_by(level=level).first()
        return message[0]
    return None


def has_level(level: str) -> bool:
    is_exists = session.query(exists().where(Course.level == level)).scalar()
    return is_exists


def get_answer(level: str) -> str:
    answer = session.query(Course.answer).filter_by(level=level).one()
    return answer[0]


def get_next(level: str) -> str:
    next_level = session.query(Course.next_level).filter_by(level=level).one()
    if next_level[0] is None:
        return None
    else:
        return next_level[0].split(',')


def has_image(level):
    image = session.query(Course.image).filter_by(level=level).one()
    return image[0] is not None


def get_image(level: str):
    pic = open('files/' + level + '.png', 'rb')
    return pic
