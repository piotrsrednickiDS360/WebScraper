# syntax=docker/dockerfile:1

FROM python:3.9

# Environmental variables
ENV DJANGO_SUPERUSER_PASSWORD=rootroot
ENV DJANGO_SUPERUSER_EMAIL=example@example.com
ENV DJANGO_SUPERUSER_USERNAME=adminadmin
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installing requirements
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

# Using gunicorn for heroku as a dyno
CMD gunicorn TradingSupport.wsgi:application