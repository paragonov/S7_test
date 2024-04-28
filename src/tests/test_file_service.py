import csv
from datetime import date
from pathlib import Path

from src.entities import DBStorage, JsonStorage
from src.file_service.service import FileService
from src.settings import settings

file_service = FileService()


async def test_get_json_storage():
    with open(settings.file_paths.PATH_TO_TEST_FILE) as f:
        file_service._file_name = Path(settings.file_paths.PATH_TO_TEST_FILE).stem
        file_service._reader = csv.DictReader(f, delimiter=";")
        json_storage = await file_service.get_json_storage()

    assert json_storage == JsonStorage(
        flt=1223,
        date="2022-11-29",
        dep="DME",
        prl=[
            {
                "num": "1",
                "surname": "IVANOV",
                "firstname": "IVAN",
                "bdate": "11NOV73",
            },
            {
                "num": "2",
                "surname": "PETROV",
                "firstname": "ALEXANDER",
                "bdate": "13JUL79",
            },
            {
                "num": "3",
                "surname": "BOSHIROV",
                "firstname": "RUSLAN",
                "bdate": "12APR78",
            },
        ],
    )


async def test_get_db_storage():
    with open(settings.file_paths.PATH_TO_TEST_FILE) as f:
        file_service._file_name = Path(settings.file_paths.PATH_TO_TEST_FILE).stem
        file_service._reader = csv.DictReader(f, delimiter=";")
        db_storage = await file_service.get_db_storage()

    assert db_storage == DBStorage(
        file_name=file_service._file_name,
        flt=1223,
        depdate=date(2022, 11, 29),
        dep="DME",
    )
