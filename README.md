# accumulated-customer-support

AI customer support system with STT, and auto-generated documentation based on collected support history.

## Install

### Create Containers

```sh
docker compose up --build
```

### Install Audio Recorder

```sh
sudo apt install portaudio19-dev
pip install -r recorder/requirements.txt
```

### Classification

```sh
pip install -r classify/requirements.txt
```

## Run

```sh
./main.py
```

## Development
### Test Audio Recorder (Pyaudio)
#### Run python

```sh
python recorder/main.py
```

### Test Whisper.cpp
#### Place audio file

Place audio file in `in` directory.

#### Run whisper.cpp

```sh
docker compose up
docker compose exec whisper bash -c "./fromfile.sh"
```

#### Open text files.

Open .txt files in `out` directory.

### Test Classification
```sh
cd classify
python trainer.py
python main.py
```

#### Test another input
1. Open `main.py`
2. Modify `test_report`