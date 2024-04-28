from asyncio import current_task

from sqlalchemy.ext.asyncio import async_scoped_session

from src.database.db_service import session_factory


async def get_session():
    session = async_scoped_session(
        session_factory=session_factory,
        scopefunc=current_task,
    )
    yield session
    await session.close()
