FROM python:3.6.12-alpine3.12 

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN pip3 install pika
RUN pip3 install redis
RUN pip3 install flask
RUN pip3 install requests
RUN git clone https://github.com/hhursev/recipe-scrapers.git
RUN pip3 install recipe-scraper

ENV PYTHONUNBUFFERED=1

RUN mkdir /worker
WORKDIR /worker
copy worker-server.py /worker
CMD  python3 worker-server.py
