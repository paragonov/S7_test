from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.db_service import db_service
from src.dependencies import get_session

router = APIRouter()


@router.get("/flights/{date}")
async def get_all_flights_for_date(
    date: str,
    db_session: AsyncSession = Depends(get_session),
):
    converted_date = date
    logger.info(f"Start get all flights for date: {converted_date}")
    if not (flights := await db_service.get_all_flights_for_date(db_session, converted_date)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Flights not found")

    return flights
