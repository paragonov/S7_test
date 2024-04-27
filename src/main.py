import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from src.file_service.service import file_service
from src.router import router
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("")
    asyncio.create_task(file_service.run(15))  # noqa
    yield


app = FastAPI(title="S7_test", version="1.0.0", debug=settings.DEBUG, lifespan=lifespan)
app.include_router(router, prefix="/api/v1/auth")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
