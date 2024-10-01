# トラブルシューティング

## WSL 環境下で Pyaudio がオーディオインターフェースを発見できない

1. 管理者権限 Powershell で`wsl --version`を入力し、WSLg が導入されている事を確認
2. Ubuntu で、

```sh
sudo apt update
sudo apt upgrade -y
sudo apt install -y pulseaudio alsa-utils
```

3. 動作チェック

```sh
pulseaudio --check
pactl info
pactl list short sinks
pactl list short sources
```
