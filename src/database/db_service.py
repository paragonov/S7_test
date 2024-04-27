from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from src import FlightsModel
from src.settings import settings


class DatabaseService:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def db_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def get_all_flights_for_date(self, date):
        async with self.db_session() as session:
            stmt = select(FlightsModel).where(FlightsModel.depdate == date)
            result = await session.execute(stmt)
            model = result.scalars().all()
            return model

    async def create(self, model, data):
        async with self.db_session() as session:
            new_model = model(**data)
            session.add(new_model)

            await session.commit()


db_service = DatabaseService(
    url=settings.database.DATABASE_URL,
    echo=settings.DEBUG,
)
