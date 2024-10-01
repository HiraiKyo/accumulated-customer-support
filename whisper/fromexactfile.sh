#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file_name> <output_file_name>"
    exit 1
fi

filename=`basename $1 | sed 's/\.[^\.]*$//'`

INPUT_FILE=$1
OUTPUT_FILE=$2

# 16kHzのWAVファイルに変換
ffmpeg -i ${INPUT_FILE} -ar 16000 -ac 1 -c:a pcm_s16le ./conv_${filename}.wav

echo "Whisper.cpp decoding started: $1"
# 文字起こし処理実行
./main -m models/ggml-small.bin -f ./conv_${filename}.wav -l ja > ${OUTPUT_FILE}

# 変換ファイル削除
rm -f ./conv_${filename}.wav

echo "Whisper.cpp decoding finished: $2"