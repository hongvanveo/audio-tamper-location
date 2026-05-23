#!/usr/bin/env python3
from pathlib import Path

from self_marking import (
    DEFAULT_BLOCK_SAMPLES,
    digest_payload_with_sign,
    embed_signature,
    ensure_block_size,
    full_block_count,
    load_text_bytes,
    mark_result,
    read_wav,
    signature_bytes,
    write_wav,
)


AUDIO_FILE = ""
SIGN_FILE = ""
OUTPUT_FILE = "marked.wav"
BLOCK_SAMPLES = DEFAULT_BLOCK_SAMPLES


def main():
    if not AUDIO_FILE or not SIGN_FILE:
        raise SystemExit("Hay dien ten file vao cac dong TODO trong embed_task.py")

    ensure_block_size(BLOCK_SAMPLES)
    sign_bytes = load_text_bytes(SIGN_FILE)
    wav_data = read_wav(AUDIO_FILE)
    count = full_block_count(wav_data.samples, BLOCK_SAMPLES)
    if count == 0:
        raise SystemExit("file qua ngan, khong du mot block")

    for block_index in range(count):
        digest = digest_payload_with_sign(
            wav_data.samples,
            block_index,
            BLOCK_SAMPLES,
            sign_bytes,
        )
        embed_signature(
            wav_data.samples,
            block_index,
            BLOCK_SAMPLES,
            signature_bytes(digest),
        )

    write_wav(OUTPUT_FILE, wav_data)
    mark_result("PASS_MARKED_CREATED")
    print(f"marked={OUTPUT_FILE}")


if __name__ == "__main__":
    main()
