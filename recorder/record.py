#!/usr/bin/env python3
# mypy: ignore-errors
import pyaudio
import wave

CHUNK = 2**10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FILENAME="record.wav"
OUTDIR="../in"

def record():
    """
    音声を録音してmp3形式で保存する
    """
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    print("Recording...")
    frames = []

    # Keep recording till the user enters any key
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if input():
            break

    print("Finished recording. Outputting file...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(f"{OUTDIR}/{FILENAME}", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"File saved successfully at {OUTDIR}/{FILENAME}")

if __name__ == '__main__':
    record()