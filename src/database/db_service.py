from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src import FlightsModel
from src.settings import settings

engine = create_async_engine(
    url=settings.database.DATABASE_URL,
    echo=settings.DEBUG,
)
session_factory = async_sessionmaker(
    bind=engine,
)


class DatabaseService:
    @staticmethod
    async def get_all_flights_for_date(session: AsyncSession, date: str) -> list[FlightsModel]:
        stmt = select(FlightsModel).where(FlightsModel.depdate == date)
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create(session: AsyncSession, model: Type[FlightsModel], data: dict) -> None:
        new_model = model(**data)
        session.add(new_model)
        await session.commit()


db_service = DatabaseService()
