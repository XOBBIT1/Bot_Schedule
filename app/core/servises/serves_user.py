import datetime
import logging

from app.settings.bd.models import Trainings, Users

from app.settings.bd.session_to_postgres import create_dbsession

db_session = create_dbsession()


async def check_user(message):
    with db_session as session:
        try:
            return session.query(Users).filter_by(chat_id=message.chat.id).count()
        except Exception as e:
            logging.info(e)
            session.rollback()


async def create_user(message, user_name: str):
    try:
        db_session.add(Users(
            user_name=user_name,
            chat_id=message.chat.id,
            created_at=datetime.datetime.now(),
            last_appear=datetime.datetime.now()
        ))
        db_session.commit()
        db_session.close()
    except Exception as e:
        logging.info(e)
        db_session.rollback()


async def get_user_name(message):
    with db_session as session:
        try:
            chat_ids = session.query(Users).filter_by(chat_id=message.chat.id)
            for chat_id in chat_ids:
                return chat_id.user_name
        except Exception as e:
            logging.info(e)
            db_session.rollback()


async def sign_up_user_for_training(message, training_id: str):
    try:
        training = db_session.query(Trainings).filter_by(id=training_id).first()

        if training:
            user = db_session.query(Users).filter_by(chat_id=message.chat.id).first()
            if user:
                training.user = user
                training.booked = True
                db_session.commit()
    except Exception as e:
        logging.info(e)
        db_session.rollback()


async def cancel_training(message, training_id: str):
    try:
        training = db_session.query(Trainings).filter_by(id=training_id).first()

        if training:
            user = db_session.query(Users).filter_by(chat_id=message.chat.id).first()
            if user:
                training.user = None
                training.booked = False
                db_session.commit()
    except Exception as e:
        logging.info(e)
        db_session.rollback()


async def user_trainings(message):
    try:
        user = db_session.query(Users).filter_by(chat_id=message.chat.id).first()
        return user.trainings
    except Exception as e:
        logging.info(e)
        db_session.rollback()
