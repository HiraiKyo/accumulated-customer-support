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

## Run

### Place audio file

Place audio file in `in` directory.

### Run whisper.cpp

```sh
docker compose up
docker compose exec whisper bash -c "./fromfile.sh"
```

### Open text files.

Open .txt files in `out` directory.
