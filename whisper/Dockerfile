FROM gcc:12.2.0-bullseye

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV OUTDIR=/var/tmp/out
RUN mkdir -p $OUTDIR
RUN chown -R 1000:1000 $OUTDIR

# Update packages
RUN apt-get update
RUN apt-get install -y vim git git-secrets ffmpeg

# タイムゾーン設定
ENV TZ $TIMEZONE

# ユーザー追加
RUN groupadd -g 1000 cppuser && \
    useradd -m -s /bin/bash -u 1000 -g 1000 cppuser

# リソース取得
RUN git clone https://github.com/ggerganov/whisper.cpp.git
# 権限変更
RUN chown -R 1000:1000 /usr/src/app/whisper.cpp

# ユーザー切り替え
USER cppuser
WORKDIR /usr/src/app/whisper.cpp

# モデルダウンロード
COPY ./fromfile.sh .
RUN bash ./models/download-ggml-model.sh large-v1
RUN make