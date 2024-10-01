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

class AudioRecorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        self.write_to_stream()
        return (None, pyaudio.paContinue)

    def write_to_stream(self):
        # TODO: streaming to whisper.cpp by StreamSocket
        pass

    def write_to_file(self):
        if len(self.frames) == 0:
            print("Recorded chunks missing, failed to output.")

        wf = wave.open(f"{OUTDIR}/{FILENAME}", "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        print(f"File saved successfully at {OUTDIR}/{FILENAME}")

    def start_recording(self):
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=0,
            frames_per_buffer=CHUNK,
            stream_callback=self.callback
        )
        self.is_recording = True
        print("Recording...")

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.is_recording = False
        self.p.terminate()
        self.write_to_file()

if __name__ == "__main__":
    recorder = AudioRecorder()
    try:
        print("Press Enter to start recording...")
        input()
        recorder.start_recording()

        print("Press Enter to stop recording...")
        input()
    except Exception as e:
        print(e)
    finally:
        recorder.stop_recording()
