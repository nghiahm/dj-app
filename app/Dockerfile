FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./src/pyproject.toml .

RUN pip install poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction

COPY ./src  .

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]