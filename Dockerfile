FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y python-pip && \
    apt-get clean && \
    apt-get autoclean

RUN pip install --upgrade pip

RUN apt-get install -y libftdi-dev && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
