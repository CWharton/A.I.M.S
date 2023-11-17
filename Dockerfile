FROM python:latest

MAINTAINER Chris Wharton
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY !f!_09(rpz8sr9xx=yd@mh*lj+5iqk3%6k)8r&6gm#oku$5y@j
ENV DJANGO_DEBUG False
ENV APP_URL http://aims.automax.locals

RUN pip install --upgrade pip
ADD requirements.txt /code/
RUN pip install -r requirements.txt

COPY . .
COPY ./.docker/aims_scripts/entrypoint.sh .

EXPOSE 8000

CMD /bin/bash /entrypoint.sh
