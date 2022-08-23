# syntax=docker/dockerfile:1
FROM python:3.9

ENV DJANGO_SUPERUSER_PASSWORD=rootroot
ENV DJANGO_SUPERUSER_EMAIL=example@example.com
ENV DJANGO_SUPERUSER_USERNAME=adminadmin
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

CMD gunicorn TradingSupport.wsgi:application --bind 0.0.0.0:$PORT