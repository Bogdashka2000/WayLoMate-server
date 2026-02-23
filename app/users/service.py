from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.users.models import User
from fastapi import APIRouter, Response, Depends, UploadFile, File, status, HTTPException
from app.languages.models import Language
from app.hobbies.models import Hobby
from app.travel_goals.models import TravelGoal
from app.users.schemas import UserRegistrationScheme, UserAvaibleInfo
from app.users.associative_tables.models import UserHobby, UserTravelGoal, UserLanguage
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from app.configurator import get_static_path

class UserService:

    @classmethod
    async def find_user_one_or_none(cls, **fltr):
        async with async_session_maker() as session:
            check = await session.execute(
                select(User).filter_by(**fltr)
            )
            return check.scalar_one_or_none()


    @classmethod
    async def change_user_info(cls, user, **new_info):
         async with async_session_maker() as session:   
            check = await session.execute(select(User).filter_by(id=user.id))
            user_in_db = check.scalars().one()

            if not user_in_db:
                 raise HTTPException(status_code=404, detail="Пользователь не найден")

            for key, value in new_info.items():
                if hasattr(user_in_db, key):
                    setattr(user_in_db, key, value)
            
            await session.commit()
            await session.refresh(user_in_db)
        
            return user_in_db


    @classmethod
    async def change_user_avatar(cls, user, image_name):
        async with async_session_maker() as session:   
            check = await session.execute(select(User).filter_by(id=user.id))
            user_in_db = check.scalars().one()

            if not user_in_db:
                 raise HTTPException(status_code=404, detail="Пользователь не найден")
            user_in_db.avatar_image_url = f"{get_static_path()["static_dir_avatar_for_link"]}{image_name}"

            await session.commit()
            await session.refresh(user_in_db)
            return user_in_db

    @classmethod
    async def change_user_header(cls, user, header_name):
        async with async_session_maker() as session:   
            check = await session.execute(select(User).filter_by(id=user.id))
            user_in_db = check.scalars().one()

            if not user_in_db:
                 raise HTTPException(status_code=404, detail="Пользователь не найден")
            user_in_db.header_image_url = f"{get_static_path()["static_dir_header_for_link"]}{header_name}"

            await session.commit()
            await session.refresh(user_in_db)
            return user_in_db

    @classmethod
    async def remove_user(cls, user):
        async with async_session_maker() as session:   
            check = await session.execute(select(User).filter_by(id=user.id))
            user_in_db = check.scalars().one()

            if not user_in_db:
                 raise HTTPException(status_code=404, detail="Пользователь не найден")

            await session.delete(user_in_db)
            await session.commit()

            return user_in_db

    @classmethod
    async def find_hobbies_by_user_id(cls, user_id):
        async with async_session_maker() as session:   
            check = await session.execute(select(User).filter_by(id=user_id))
            user_in_db = check.scalars().one_or_none()

            if not user_in_db:
                 raise HTTPException(status_code=404, detail="Пользователь не найден")

            hobby_result = await session.execute(
                select(UserHobby)
                .options(joinedload(UserHobby.hobby))
                .where(UserHobby.user_id == user_id)
            )
            hobby = hobby_result.scalars().all()
            return [rel.hobby for rel in hobby]

    @classmethod
    async def find_goals_by_user_id(cls, user_id):
        async with async_session_maker() as session:   
            check = await session.execute(select(User).filter_by(id=user_id))
            user_in_db = check.scalars().one()

            goals_result = await session.execute(
                select(UserTravelGoal)
                .options(joinedload(UserTravelGoal.travel_goal))
                .where(UserTravelGoal.user_id == user_id)
            )
            goal = goals_result.scalars().all()
            return [rel.travel_goal for rel in goal]
 
    @classmethod
    async def find_languages_by_user_id(cls, user_id):
        async with async_session_maker() as session:   
            check = await session.execute(select(User).filter_by(id=user_id))
            user_in_db = check.scalars().one()   

            language_result = await session.execute(
                select(UserLanguage)
                .options(joinedload(UserLanguage.language))
                .where(UserLanguage.user_id == user_id)
            )
            language = language_result.scalars().all()
            return [rel.language for rel in language]  

    @classmethod
    async def find_all_validation_users(cls, **fltr):
        async with async_session_maker() as session:
            check = await session.execute(
                select(User).filter_by(**fltr)
            )
            user = check.scalars().all()
            return [UserAvaibleInfo.model_validate(u) for u in user]



    @classmethod
    async def add_new_user(cls, user_data: UserRegistrationScheme):
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



            
                