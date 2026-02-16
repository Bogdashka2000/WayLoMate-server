from sqlalchemy import select
from app.users.models import User
from app.languages.models import Language
from app.hobbies.models import Hobby
from app.travel_goals.models import TravelGoal
from app.users.schemas import UserRegistrationScheme
from app.users.associative_tables.models import UserHobby, UserTravelGoal, UserLanguage
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError

class UserService:

    @classmethod
    async def find_user_one_or_none(cls, **fltr):
        async with async_session_maker() as session:
            check = await session.execute(
                select(User).filter_by(**fltr)
            )
            return check.scalar_one_or_none()


    @classmethod
    async def addNewUser(cls, user_data: UserRegistrationScheme):
        async with async_session_maker() as session:
            user = User(
                **user_data.model_dump(
                    exclude={
                        "hobbies",
                        "goals",
                        "languages"
                    }
                )
            )

            session.add(user)
            await session.flush()

            if user_data.hobbies:
                hobbies_result = await session.execute(
                    select(Hobby).where(Hobby.id.in_(user_data.hobbies))
                )
                existing_hobbies = hobbies_result.scalars().all()

                for hobby in existing_hobbies:
                    user_hobby = UserHobby(user_id = user.id, hobby_id = hobby.id)
                    session.add(user_hobby)
                
            if user_data.goals:
                goals_result = await session.execute(
                    select(TravelGoal).where(TravelGoal.id.in_(user_data.goals))
                )
                existing_goals = goals_result.scalars().all()

                for goal in existing_goals:
                    user_goal = UserTravelGoal(user_id = user.id, travel_goal_id=goal.id)
                    session.add(user_goal)

            if user_data.languages:
                language_result = await session.execute(
                    select(Language).where(Language.id.in_(user_data.languages))
                )

                existing_languages = language_result.scalars().all()

                for language in existing_languages:
                    user_lang = UserLanguage(user_id = user.id, language_id=language.id)
                    session.add(user_lang)

            await session.commit()
            await session.refresh(user)
            return user



            
                