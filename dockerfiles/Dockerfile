FROM python:3.12.3-slim
COPY requirements.txt /tmp

WORKDIR /app
RUN set -x && \
    apt-get update && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

COPY ./src /app/src
