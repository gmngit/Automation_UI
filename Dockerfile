FROM python:3.12-slim

WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app
