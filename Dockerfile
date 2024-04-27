FROM python:3.12-alpine

WORKDIR /app

COPY pyproject.toml pyproject.toml ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install

COPY . .
