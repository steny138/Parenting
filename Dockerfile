FROM python:3.10-slim

ARG PORT=5000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.2.0
# create the app directory - and switch to it
RUN mkdir -p /app

COPY pyproject.toml /app 

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

# system deps installation
RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    brotli \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev 

# poetry installation
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 - 

ENV PATH "${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    rm -rf /root/.cache/

# copy project
COPY . /app/

# expose port 8000
EXPOSE 8000

CMD ["uvicorn", "parenting.app:app", "--host", "0.0.0.0","--port", "${PORT}", "--log-config", "./parenting/logging.conf", "--workers", "2"]