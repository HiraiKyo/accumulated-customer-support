#!/usr/bin/env python

# mypy: ignore-errors

import os
import argparse
from faster_whisper import WhisperModel, BatchedInferencePipeline
import time
import json

# MODEL_NAME = "small"
MODEL_NAME="large-v3"
MODEL_PATH=f"/var/tmp/models/whisper-{MODEL_NAME}"

def transcribe(wav_file, verbose=False, batched=False):
    model = WhisperModel(
        MODEL_NAME,
        device="cpu",
        compute_type="int8",
        cpu_threads=os.cpu_count(),
        download_root=MODEL_PATH
    )
    if batched:
        model = BatchedInferencePipeline(model=model, language="ja")

    start_time = time.time()
    if batched:
        segments, info = model.transcribe(
            wav_file,
            language="ja",
            batch_size=16
        )
    else:
        segments, info = model.transcribe(
            wav_file,
            language="ja",
            vad_filter=True,
            beam_size=5,
        )

    if verbose:
        # infoの内容を表示
        print(json.dumps(info._asdict(), ensure_ascii=False, indent=2))

    for segment in segments:
        line = ""
        if verbose:
            time_lapsed = time.time() - start_time
            line = f"[{time_lapsed:.2f}] [{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}"
        else:
            line = segment.text
        print(line)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-m", type=str, help="モデル名")
    argparser.add_argument("-w", type=str, help="wavファイル名")
    argparser.add_argument("--verbose", action="store_true", help="冗長な出力を行うかどうか")
    argparser.add_argument("--batched", action="store_true", help="バッチモデルを利用するか")
    args = argparser.parse_args()
    try:
        transcribe(args.w, verbose=args.verbose, batched=args.batched)
    except KeyboardInterrupt:
        print("中断されました")