FROM python:latest

MAINTAINER Chris Wharton

ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY !f!_09(rpz8sr9xx=yd@mh*lj+5iqk3%6k)8r&6gm#oku$5y@j
ENV DJANGO_DEBUG False
ENV APP_URL http://aims.automax.locals

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/
#COPY ./.docker/aims_scripts/entrypoint.sh /code/

EXPOSE 8000

CMD /bin/bash /code/entrypoint.sh