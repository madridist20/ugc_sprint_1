FROM python:3.10.6-slim

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  apt-get update \
     && apt-get install -y gcc \
     && pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .
COPY core/docker.env core/.env


ENTRYPOINT ["python", "main.py"]

