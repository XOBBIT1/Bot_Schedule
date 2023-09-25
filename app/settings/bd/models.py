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
    owner_trainings = relationship("Trainings", secondary="owner_trainings", collection_class=list)
    user_trainings = relationship("Trainings", secondary="user_trainings", collection_class=list)


class Trainings(Base):
    __tablename__ = "Trainings"

    id = db.Column(db.BigInteger, primary_key=True)
    training_time = db.Column("training_time", db.String)
    training_owner = db.Column("training_owner", db.String)
    user_id = db.Column(db.BigInteger, db.ForeignKey("Users.id"))
    owner_id = db.Column(db.BigInteger, db.ForeignKey("Users.id"))
    user = relationship("Users", back_populates="user_trainings")
    owner = relationship("Users", back_populates="owner_trainings")
    booked = db.Column(db.Boolean, default=False)
