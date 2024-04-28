import json
from dataclasses import dataclass
from datetime import date


@dataclass
class JsonStorage:
    flt: int
    date: str
    dep: str
    prl: list[dict]

    def convert_to_json(self):
        return json.dumps(self.__dict__)


@dataclass
class DBStorage:
    file_name: str
    flt: int
    depdate: date
    dep: str
