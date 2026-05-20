# audio-tamper-location

Labtainer lab for fragile self-marking audio tamper localization.

## Install in Labtainer

```bash
imodule https://raw.githubusercontent.com/hongvanveo/audio-tamper-location/main/imodule_audio-tamper-location.tar
labtainer -r audio-tamper-location
```

## Student workflow

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav --seconds 5
python3 mark_blocks.py cover.wav marked.wav
python3 verify_blocks.py marked.wav
python3 tamper_audio.py marked.wav tampered.wav --start 3.20 --end 3.80
python3 verify_blocks.py tampered.wav
checkwork
```

Checkwork has six goals:

- `cover_created`
- `marked_created`
- `signature_found`
- `clean_audio_ok`
- `tampered_created`
- `tamper_localized`
