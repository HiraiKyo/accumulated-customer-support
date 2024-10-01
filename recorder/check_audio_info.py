# mypy: ignore-errors
import pyaudio
import sys

def print_audio_info():
    try:
        p = pyaudio.PyAudio()
        
        print(f"PyAudio version: {pyaudio.__version__}")
        # print(f"PortAudio version: {p.get_portaudio_version()}")
        # print(f"PortAudio version text: {p.get_portaudio_version_text()}")
        
        host_api_count = p.get_host_api_count()
        print(f"\nNumber of host APIs: {host_api_count}")
        
        for i in range(host_api_count):
            info = p.get_host_api_info_by_index(i)
            print(f"\nHost API {i}:")
            print(f"  Name: {info['name']}")
            print(f"  Default input device: {info['defaultInputDevice']}")
            print(f"  Default output device: {info['defaultOutputDevice']}")
        
        device_count = p.get_device_count()
        print(f"\nNumber of devices: {device_count}")
        
        for i in range(device_count):
            try:
                info = p.get_device_info_by_index(i)
                print(f"\nDevice {i}:")
                print(f"  Name: {info['name']}")
                print(f"  Host API: {info['hostApi']}")
                print(f"  Max input channels: {info['maxInputChannels']}")
                print(f"  Max output channels: {info['maxOutputChannels']}")
                print(f"  Default sample rate: {info['defaultSampleRate']}")
            except IOError as e:
                print(f"Error getting info for device {i}: {e}")
        
        p.terminate()
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Python version: {sys.version}")
        print(f"PyAudio path: {pyaudio.__file__}")

if __name__ == "__main__":
    print_audio_info()