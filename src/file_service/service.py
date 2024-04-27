import asyncio
import csv
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

import aiocsv
import aiofiles
from loguru import logger

from src import FlightsModel
from src.database.db_service import db_service
from src.entities import JsonStorage, DBStorage
from src.settings import BASE_DIR, settings


class FileService:
    reader = None
    __file_name = None

    async def run(self, schedule_time):
        while True:
            if list_file_names := os.listdir(BASE_DIR / "ln"):
                for file_name in list_file_names:
                    with open(settings.file_paths.PATH_TO_FILES + file_name, "r") as f:
                        self.reader = csv.reader(f)
                        self.__file_name = Path(file_name).stem

                    try:
                        json_storage = await self.get_json_storage()
                        db_storage = await self.get_db_storage()

                        await self.converting_file_to_json(json_storage)
                        await self.write_file_to_db(db_storage)

                    except Exception as ex:
                        logger.exception(ex)
                        logger.error(f"Error has occurred. Ex: {str(ex)}")
                        await self.move_file_to_another_dir(
                            settings.file_paths.PATH_TO_FILES + f"{self.__file_name}.csv",
                            settings.file_paths.PATH_TO_ERR + f"{self.__file_name}.csv"
                        )

                    else:
                        await self.move_file_to_another_dir(
                            settings.file_paths.PATH_TO_FILES + f"{self.__file_name}.csv",
                            settings.file_paths.PATH_TO_OK + f"{self.__file_name}.csv"
                        )

            await asyncio.sleep(schedule_time)

    async def converting_file_to_json(self, json_storage):
        json_file_name = await self.get_json_file_name()
        async with aiofiles.open(json_file_name, "w") as f:
            await f.write(json.dumps(json_storage.__dict__))

    @staticmethod
    async def write_file_to_db(db_storage):
        await db_service.create(FlightsModel, db_storage.__dict__)

    @staticmethod
    async def move_file_to_another_dir(old_dir, new_dir):
        shutil.move(old_dir, new_dir)

    async def get_json_storage(self):
        date, flt, dep = await self.get_data_from_file_name_for_json()
        prl = [
            {
                "num": row[0].split(";")[0],
                "surname": row[0].split(";")[1],
                "firstname": row[0].split(";")[2],
                "bdate": row[0].split(";")[3],
            }
            for row in self.reader
        ][1:]
        return JsonStorage(
            flt=flt,
            date=date,
            dep=dep,
            prl=prl
        )

    async def get_db_storage(self):
        depdate, flt, dep = await self.get_data_from_file_name_for_db()
        return DBStorage(
            file_name=self.__file_name,
            flt=flt,
            depdate=depdate,
            dep=dep
        )

    async def get_data_from_file_name_for_json(self):
        date, flt, dep = self.__file_name.split("_")
        date = (await self.validate_date(date)).strftime("%Y-%m-%d")
        return date, flt, dep

    async def get_data_from_file_name_for_db(self):
        date, flt, dep = self.__file_name.split("_")
        return await self.validate_date(date), flt, dep

    async def get_json_file_name(self):
        return f"{settings.file_paths.PATH_TO_JSON_FILES}/{self.__file_name}.json"

    @staticmethod
    async def validate_date(date):
        try:
            return datetime.strptime(date, "%Y%m%d").date()
        except Exception as ex:
            logger.error(f"Invalid date. Date: {date}")
            raise ex


file_service = FileService()
