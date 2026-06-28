FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    dos2unix \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY app ./app
COPY commands ./commands
COPY migrations ./migrations
COPY alembic.ini ./alembic.ini

RUN dos2unix /app/commands/*.sh \
    && chmod +x /app/commands/*.sh

CMD ["/app/commands/run_web_server.sh"]

