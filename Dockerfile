FROM ubuntu:16.04

LABEL "maintainer"="lanpn <lanpn@vng.com.vn>"

# System dependencies
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip
RUN pip3 install pipenv

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Python dependencies
ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app
EXPOSE 5000
CMD gunicorn --config configs/gunicorn.py app:app
