FROM python:3.6-slim-stretch

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN pip3 install pika
RUN pip3 install redis
RUN pip3 install flask
RUN pip3 install requests
RUN pip3 install --upgrade pip
RUN git clone https://github.com/hhursev/recipe-scrapers.git
RUN cd recipe-scrapers
RUN pip3 install recipe-scrapers
#CMD python3 setup.py install --yes USE_AVX_INSTRUCTIONS

ENV PYTHONUNBUFFERED=1

RUN mkdir /worker
WORKDIR /worker
copy worker-server.py /worker
CMD  python3 worker-server.py
