from asyncio import current_task
from datetime import date

import pytest
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine

from src import Base, FlightsModel
from src.settings import settings

engine = create_async_engine(
    url=settings.database.TEST_DATABASE_URL,
    echo=settings.DEBUG,
)
session_factory = async_sessionmaker(
    bind=engine,
)


async def get_test_session():
    session = async_scoped_session(
        session_factory=session_factory,
        scopefunc=current_task,
    )
    yield session
    await session.close()


@pytest.fixture(scope="session")
async def create_models():
    session = async_scoped_session(
        session_factory=session_factory,
        scopefunc=current_task,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    flights_models = [
        FlightsModel(
            id=1,
            file_name="test_file1.csv",
            flt=1234,
            depdate=date(2022, 1, 1),
            dep="test1",
        ),
        FlightsModel(
            id=2,
            file_name="test_file2.csv",
            flt=12345,
            depdate=date(2022, 1, 2),
            dep="test2",
        ),
        FlightsModel(
            id=3,
            file_name="test_file3.csv",
            flt=12346,
            depdate=date(2022, 11, 23),
            dep="test3",
        ),
        FlightsModel(
            id=4,
            file_name="test_file3.csv",
            flt=12346,
            depdate=date(2022, 11, 23),
            dep="test3",
        ),
    ]

    for model in flights_models:
        session.add(model)
        await session.commit()

    stmt = select(FlightsModel)
    result = await session.execute(stmt)
    logger.info(f"Created model: {len(result.scalars().all())}")
