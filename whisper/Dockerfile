FROM gcc:12.2.0-bullseye

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV OUTDIR=/var/tmp/out
RUN mkdir -p $OUTDIR
RUN chown -R 1000:1000 $OUTDIR

# Update packages
RUN apt-get update
RUN apt-get install -y vim git git-secrets ffmpeg
# Linux用のWhisper.cppビルドツールを追加
RUN apt-get install -y libopenblas-dev

# タイムゾーン設定
ENV TZ $TIMEZONE

# リソース取得
RUN git clone https://github.com/ggerganov/whisper.cpp.git

WORKDIR /usr/src/app/whisper.cpp

# モデルダウンロード
RUN bash ./models/download-ggml-model.sh small

COPY ./* .
RUN pip install -r requirements.txt

RUN make CFLAGS="-DGGML_USE_OPENBLAS -march=x86-64 -mtune=generic" OPENBLAS=1