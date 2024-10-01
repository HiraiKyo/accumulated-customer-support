# mypy: ignore-errors
import pyaudio

p = pyaudio.PyAudio()

print("Available devices:")
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_host_api_device_index(0, i)
    print(f"デバイス {i}: {dev['name']}")
    print(f"  入力チャンネル: {dev['maxInputChannels']}")
    print(f"  出力チャンネル: {dev['maxOutputChannels']}")
    print(f"  デフォルト サンプルレート: {dev['defaultSampleRate']}")
    print()

p.terminate()