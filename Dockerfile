FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.3.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

COPY pyproject.toml poetry.lock ./
 
RUN poetry install --only main --no-root

FROM python:3.13-slim

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/.venv /app/.venv

COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]