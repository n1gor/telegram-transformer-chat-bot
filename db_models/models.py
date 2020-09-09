from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    middle_name = Column(String(64))
    last_name = Column(String(64), nullable=False)
    phone_number = Column(String(64), nullable=False)
    telegram_id = Column(Integer)

    def __repr__(self):
        return "<User(first name='%s', middle name='%s', last name='%s', " \
               "phone number='%s', telegram id='%s')>" % (
                self.first_name, self.middle_name, self.last_name, self.phone_number, self.telegram_id)
