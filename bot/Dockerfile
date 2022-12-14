FROM python:3.10.6-alpine

WORKDIR /usr/src/bot

COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .
