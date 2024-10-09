FROM python:3.12-slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV OUTDIR=/var/tmp/out
RUN mkdir -p $OUTDIR
RUN chown -R 1000:1000 $OUTDIR

# Update packages
RUN apt-get update && \
    apt-get install -y ffmpeg software-properties-common vim git git-secrets && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install numpy torch

# タイムゾーン設定
ENV TZ $TIMEZONE

COPY ./* .
RUN pip install -r requirements.txt
RUN chmod +x ./main.py