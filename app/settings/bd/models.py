from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "Users"

    id = db.Column(db.BigInteger, primary_key=True)
    user_name = db.Column("user_name", db.String)
    chat_id = db.Column("chat_id", db.BigInteger)
    created_at = db.Column(TIMESTAMP, default=datetime.utcnow())
    last_appear = db.Column(TIMESTAMP, default=datetime.utcnow())

    trainings = relationship("Trainings", back_populates="user")


class Trainings(Base):
    __tablename__ = "Trainings"

    id = db.Column(db.BigInteger, primary_key=True)
    training_day = db.Column("training_day", db.String)
    training_time = db.Column("training_time", db.String)
    user_id = db.Column(db.BigInteger, db.ForeignKey("Users.id"))
    booked = db.Column(db.Boolean, default=False)

    user = relationship("Users", back_populates="trainings")
