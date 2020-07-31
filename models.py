from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship

# 패스워드 암호를 위해서!!
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    like_list = Column(list)

    def __init__(self, username, email, password, **kwargs):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User('{self.id}', '{self.username}', '{self.email}')>"


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    writer = Column(String, nullable=False)
    # 나중에 하자
    # content = Column(String)
    date = Column(String)
    view = Column(String)

    def __repr__(self):
        return f"<Post('{self.id}', '{self.title}')>"

