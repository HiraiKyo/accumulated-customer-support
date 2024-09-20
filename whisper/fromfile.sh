# 指定拡張子のファイルがあるか
for _audio_file in ./*.{wav,WAV,aiff,AIFF,aac,AAC,mp3,MP3}; do

    # 指定拡張子がない場合は、以下の処理を行わない
    [ -f "$_audio_file" ] || continue

    # 拡張子なしのフォルダ
    _audio_file_name=`basename ${_audio_file} | sed 's/\.[^\.]*$//'`

    # 16kHzのWAVファイルに変換
    ffmpeg -i ${_audio_file} -ar 16000 -ac 1 -c:a pcm_s16le ./conv_${_audio_file_name}.wav

    # 文字起こし処理実行
    ./main -m models/ggml-small.bin -f ./conv_${_audio_file_name}.wav -l ja > /var/tmp/out/${_audio_file_name}.txt

    # 変換ファイル削除
    rm -f ./conv_${_audio_file_name}.wav

done