import datetime
from app.settings.bd.models import Trainings, Users


from app.settings.bd.session_to_postgres import create_dbsession

db_session = create_dbsession()


async def create_training(message, training_time: str):
    db_session.add(Trainings(
        training_time=training_time,
        training_owner=message.from_user.username
    ))
    db_session.commit()
    db_session.close()


async def create_user(message, user_name: str):
    user_count = db_session.query(Users).filter_by(chat_id=message.chat.id).count()
    if user_count > 0:
        print("User already exists")
    else:
        db_session.add(Users(
            user_name=user_name,
            chat_id=message.chat.id,
            username=message.from_user.username,
            created_at=datetime.datetime.now(),
            last_appear=datetime.datetime.now()
        ))
        db_session.commit()
        db_session.close()


async def writing_data(data: dict, model):
    db_session.add(model(**data))
    db_session.commit()
    db_session.close()
