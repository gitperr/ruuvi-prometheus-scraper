FROM python:3.13.0a3-alpine3.19

WORKDIR /

COPY ./app .

WORKDIR /app

RUN pip3 install requirements.txt && python3 main.py
