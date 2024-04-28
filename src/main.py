import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src import Base
from src.database.db_service import engine
from src.file_service.service import file_service
from src.router import router
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(file_service.run(120))
    yield


app = FastAPI(title="S7_test", version="1.0.0", debug=settings.DEBUG, lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
