#!/usr/bin/env python3
# mypy: ignore-errors
import os
import subprocess
import sys
import time
from recorder.record import AudioRecorder
import datetime
import docker
import multiprocessing
import argparse

INDIR = "in"
FILENAME = datetime.datetime.now().isoformat()

# ARGPARSE
parser = argparse.ArgumentParser()
parser.add_argument("--test", action="store_true", help="Run in test mode.")
args = parser.parse_args()

#
# 録音
#
recorder = AudioRecorder()
try:
    print("Press any key to start recording...")
    input()
    recorder.start_recording()

    print("Press any key to stop recording...")
    input()
except Exception as e:
    print(e)
finally:
    recorder.stop_recording()
    wavfile = recorder.write_to_file(INDIR, FILENAME)

#
# Whisper.cppにデコード開始をリクエスト
#
print("Connecting to Whisper.cpp docker container...")

client = docker.from_env()
service_name = "whisper"
project_name = os.path.basename(os.getcwd()) # docker-composeは暗黙的にディレクトリ名がプロジェクト名になる
container_name = f"{project_name}-{service_name}-1"

# whisperコンテナの起動確認
try:
    result = subprocess.run(['docker-compose', 'ps', '-q', service_name], capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"Container for service '{service_name}' is not running. Please start it using 'docker-compose up -d'")
        sys.exit(1)
except subprocess.CalledProcessError:
    print("Error checking docker-compose status. Make sure docker-compose is installed and you're in the correct directory.")
    sys.exit(1)

# コンテナオブジェクトを取得
container = client.containers.get(container_name)
input_file = f"/var/tmp/in/{wavfile}"
if args.test: # テストモード時はtest.mp3から実行
    input_file = "/var/tmp/in/test.mp3"
output_file = f"/var/tmp/out/{FILENAME}.txt"

whisper_log_file = f"{FILENAME}_whisper_execution.log"
def write_whisper_log(message):
    with open(whisper_log_file, "a") as log:
        log.write(f"{message}\n")

def exec_whisper():
    try:
        exec_command = f"/bin/bash ./fromexactfile.sh {input_file} {output_file}"
        print("STT starting...")
        exec_result = container.exec_run(exec_command)
        for output in exec_result.output:
            write_whisper_log(output.decode().strip())
        exit_code = exec_result.exit_code
        if exit_code != 0:
            print(f"Error executing command in container. Exit code: {exit_code}")
            return False
        print("Whisper script execution completed.")
        return True
    except Exception as e:
        print(f"An error occurred while trying to execute the command in the container: {e}")
        return False

whisper_proc = multiprocessing.Process(target=exec_whisper, args=())
whisper_proc.start()

#
# 出力ファイルをreadlineする
#
host_output_file = f"./out/{FILENAME}.txt"
while not os.path.exists(host_output_file):
    time.sleep(1)
print("Reading output text...")
with open(host_output_file, 'r') as file:
    while True:
        try:
            line = file.readline()
            if not line:
                time.sleep(1)
                continue
            print(line.strip())
        except KeyboardInterrupt:
            if whisper_proc.is_alive():
                whisper_proc.terminate()
            break

print(f"Read output file here: out/{FILENAME}.txt")