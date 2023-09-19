# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.17

ENV FASTAPI_ENV=${FASTAPI_ENV} \
  # python:
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.5.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apk update && \
    apk add nmap-ncat && \
    apk --update add bash && \
    apk add dos2unix

RUN pip install "poetry==$POETRY_VERSION" && poetry --version
RUN pip install python-dotenv

WORKDIR /stats_servise

COPY pyproject.toml /stats_servise
COPY poetry.lock /stats_servise

RUN poetry install --no-root

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

ENTRYPOINT ["/entrypoint.sh"]


