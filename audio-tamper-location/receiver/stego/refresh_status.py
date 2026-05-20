#!/usr/bin/env python3
from pathlib import Path


WORKDIR = Path.home() / "stego"
RESULT = Path.home() / ".local" / "result" / "tamper_location_check.txt"


def main():
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    tokens = []
    if (WORKDIR / "cover.wav").is_file() and (WORKDIR / "cover.wav").stat().st_size > 0:
        tokens.append("PASS_COVER_CREATED")
    if (WORKDIR / "marked.wav").is_file() and (WORKDIR / "marked.wav").stat().st_size > 0:
        tokens.append("PASS_MARKED_CREATED")
    if (WORKDIR / ".signature_found_done").is_file():
        tokens.append("PASS_SIGNATURE_FOUND")
    if (WORKDIR / ".clean_audio_ok_done").is_file():
        tokens.append("PASS_CLEAN_AUDIO_OK")
    if (WORKDIR / "tampered.wav").is_file() and (WORKDIR / "tampered.wav").stat().st_size > 0:
        tokens.append("PASS_TAMPERED_CREATED")
    if (WORKDIR / ".tamper_localized_done").is_file():
        tokens.append("PASS_TAMPER_LOCALIZED")
    RESULT.write_text("\n".join(tokens) + ("\n" if tokens else ""), encoding="utf-8")


if __name__ == "__main__":
    main()

