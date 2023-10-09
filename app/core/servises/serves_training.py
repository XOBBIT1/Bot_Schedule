import logging

from app.core.servises.serves_user import db_session
from app.settings.bd.models import Trainings


async def create_training(training_time: str, training_day: str):
    try:
        db_session.add(Trainings(
            training_day=training_day,
            training_time=training_time,
        ))
        db_session.commit()
        db_session.close()
    except Exception as e:
        logging.info(e)
        db_session.rollback()


async def get_all_trainings():
    try:
        ids = db_session.query(Trainings).all()
        return ids
    except Exception as e:
        logging.info(e)
        db_session.rollback()


async def get_all_not_booked_trainings():
    try:
        ids = db_session.query(Trainings).filter_by(booked=False).all()
        return ids
    except Exception as e:
        logging.info(e)
        db_session.rollback()


async def delete_training_by_id(training_id):
    try:
        element_to_delete = db_session.query(Trainings).filter_by(id=training_id).first()
        db_session.delete(element_to_delete)
        db_session.commit()
        db_session.close()
    except Exception as e:
        logging.info(e)
        db_session.rollback()


async def checking_users_with_trainings():
    try:
        ids = db_session.query(Trainings).filter_by(booked=True).all()
        return ids
    except Exception as e:
        logging.info(e)
        db_session.rollback()
