FROM python:3.6-slim
ENV PYTHONBUFFERED 1

RUN mkdir /config
COPY config/requirements.txt /config/requirements.txt

RUN pip install -r /config/requirements.txt

RUN mkdir /src
COPY ./src/* /src/

RUN mkdir /src/app
COPY ./src/app/* /src/app/

WORKDIR /src