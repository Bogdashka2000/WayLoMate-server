from sqlalchemy import select
from app.users.models import User
from app.users.schemas import UserRegistrationScheme
from app.users.associative_tables.models import UserHobby, UserTravelGoal, UserLanguage
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError

class UserService:

    @classmethod
    async def addNewUser(cls, user_data: UserRegistrationScheme):
        async with async_session_maker() as session:
            user = User(
                **user_data.user_model_dump()
            )

            session.add(user)
            await session.flush()
            await session.commit()




            
                