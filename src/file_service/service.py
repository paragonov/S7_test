import asyncio
import csv
import json
import os
import shutil
from asyncio import current_task
from datetime import date, datetime
from pathlib import Path

from loguru import logger
from sqlalchemy.ext.asyncio import async_scoped_session

from src import FlightsModel
from src.database.db_service import db_service, session_factory
from src.entities import DBStorage, JsonStorage
from src.settings import settings


class FileService:
    _reader = None
    _file_name = None

    async def run(self, schedule_time: int) -> None:
        logger.info(f"Starting file service every {schedule_time}s")
        while True:
            logger.info("Checking ln directory...")

            if list_file_names := os.listdir(settings.file_paths.PATH_TO_LN):
                for file_name in list_file_names:
                    logger.info(f"Start process file - {file_name}")
                    try:
                        with open(settings.file_paths.PATH_TO_LN + file_name, "r") as f:
                            self._reader = csv.DictReader(f, delimiter=";")
                            self._file_name = Path(file_name).stem

                            json_storage = await self.get_json_storage()
                            db_storage = await self.get_db_storage()

                            await self.converting_file_to_json(json_storage)
                            await self.write_file_to_db(db_storage)

                    except Exception as ex:
                        logger.exception(ex)
                        logger.error(f"Error has occurred. Ex: {str(ex)}")
                        await self.move_file_to_another_dir(
                            settings.file_paths.PATH_TO_LN + file_name,
                            settings.file_paths.PATH_TO_ERR + file_name,
                        )
                    else:
                        logger.success(f"Successfuly processed file - {file_name}")
                        await self.move_file_to_another_dir(
                            settings.file_paths.PATH_TO_LN + file_name,
                            settings.file_paths.PATH_TO_OK + file_name,
                        )

            await asyncio.sleep(schedule_time)

    async def converting_file_to_json(self, json_storage: JsonStorage) -> None:
        json_file_name = await self.get_json_file_name()
        with open(json_file_name, "w") as f:
            f.write(json.dumps(json_storage.__dict__))

    @staticmethod
    async def write_file_to_db(db_storage: DBStorage) -> None:
        session = async_scoped_session(session_factory, scopefunc=current_task)
        await db_service.create(session, FlightsModel, db_storage.__dict__)

    @staticmethod
    async def move_file_to_another_dir(old_dir: str, new_dir: str) -> None:
        shutil.move(old_dir, new_dir)

    async def get_json_storage(self) -> JsonStorage:
        return JsonStorage(
            *await self.get_data_from_file_name_for_json(),
        )

    async def get_db_storage(self) -> DBStorage:
        return DBStorage(
            self._file_name,
            *await self.get_data_from_file_name_for_db(),
        )

    async def get_data_from_file_name_for_json(self) -> tuple[int, str, str, list[dict]]:
        date, flt, dep = self._file_name.split("_")
        date = (await self.validate_date(date)).strftime("%Y-%m-%d")
        prl = list(self._reader)
        return int(flt), date, dep, prl

    async def get_data_from_file_name_for_db(self) -> tuple[int, date, str]:
        date, flt, dep = self._file_name.split("_")
        return int(flt), await self.validate_date(date), dep

    async def get_json_file_name(self) -> str:
        return f"{settings.file_paths.PATH_TO_OUT}/{self._file_name}.json"

    @staticmethod
    async def validate_date(date_in_str: str) -> date:
        try:
            return datetime.strptime(date_in_str, "%Y%m%d").date()
        except Exception as ex:
            logger.error(f"Invalid date. Date: {date_in_str}")
            raise ex


file_service = FileService()
