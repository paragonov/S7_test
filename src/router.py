from fastapi import APIRouter
from loguru import logger
from src.database.db_service import db_service

router = APIRouter()


@router.get("/flights/{date}")
async def get_all_flights_for_date(
        date: str,
):
    converted_date = date
    logger.info(f"Start get all flights for date: {converted_date}")
    return await db_service.get_all_flights_for_date(converted_date)
