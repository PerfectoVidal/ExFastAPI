from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, PasswordType  # type: ignore

from src.db.base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    surname_1 = Column(String(256))
    surname_2 = Column(String(256))
    password = Column(PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt'], deprecated=['md5_crypt']), nullable=False, )  # type: ignore
    email = Column(EmailType, unique=True, index=True)
    is_superuser = Column(Boolean, default=False)
    invoices = relationship("Invoice", cascade="all", back_populates="user")  # type: ignore

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.name} {self.surname_1} {self.surname_2}'.strip()
