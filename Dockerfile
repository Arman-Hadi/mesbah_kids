FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

#COPY .repos /etc/apk/repositories

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /mesbah
WORKDIR /mesbah
COPY ./mesbah /mesbah

RUN mkdir -p /var/www/mesbah/static
RUN mkdir -p /var/www/mesbah/media
