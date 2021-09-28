from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from settings_db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname_1 = Column(String)
    surname_2 = Column(String)
    email = Column(EmailType, unique=True, index=True)
    extra_info = relationship("ExtraInfo", back_populates="users", cascade="all, delete-orphan")


class ExtraInfo(Base):
    __tablename__ = 'extra_info'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    complete = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="extra_info")


