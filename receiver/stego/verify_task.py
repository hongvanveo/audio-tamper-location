#!/usr/bin/env python3
from pathlib import Path

from self_marking import (
    DEFAULT_BLOCK_SAMPLES,
    MAGIC,
    VERSION,
    digest_payload_with_sign,
    ensure_block_size,
    extract_signature,
    fmt_time,
    full_block_count,
    load_text_bytes,
    mark_result,
    read_wav,
    seconds_for_block,
    write_marker,
)


AUDIO_FILE = ""
SIGN_FILE = ""
BLOCK_SAMPLES = DEFAULT_BLOCK_SAMPLES
QUIET_OK = True


def ranges(items):
    if not items:
        return []
    grouped = []
    start = prev = items[0]
    for item in items[1:]:
        if item == prev + 1:
            prev = item
            continue
        grouped.append((start, prev))
        start = prev = item
    grouped.append((start, prev))
    return grouped


def main():
    if not AUDIO_FILE or not SIGN_FILE:
        raise SystemExit("Hay dien ten file vao cac dong TODO trong verify_task.py")

    ensure_block_size(BLOCK_SAMPLES)
    sign_bytes = load_text_bytes(SIGN_FILE)
    wav_data = read_wav(AUDIO_FILE)
    count = full_block_count(wav_data.samples, BLOCK_SAMPLES)
    if count == 0:
        raise SystemExit("file qua ngan, khong du mot block")

    signatures = [
        extract_signature(wav_data.samples, block_index, BLOCK_SAMPLES)
        for block_index in range(count)
    ]
    has_signature = any(
        magic == MAGIC and version == VERSION
        for magic, version, _ in signatures
    )
    if not has_signature:
        print("tamper-location signature not found.")
        raise SystemExit(1)

    print("tamper-location signature found.")
    write_marker(".signature_found_done")
    mark_result("PASS_SIGNATURE_FOUND")

    tampered = []
    for block_index in range(count):
        magic, version, embedded_digest = signatures[block_index]
        current_digest = digest_payload_with_sign(
            wav_data.samples,
            block_index,
            BLOCK_SAMPLES,
            sign_bytes,
        )
        ok = magic == MAGIC and version == VERSION and embedded_digest == current_digest
        if ok:
            if not QUIET_OK:
                print(f"Block {block_index}: OK")
        else:
            tampered.append(block_index)
            print(f"Block {block_index}: TAMPERED")

    if not tampered:
        print("No modification detected.")
        if Path(AUDIO_FILE).name == "marked.wav":
            write_marker(".clean_audio_ok_done")
            mark_result("PASS_CLEAN_AUDIO_OK")
        return

    for start_block, end_block in ranges(tampered):
        start_sec, _ = seconds_for_block(start_block, BLOCK_SAMPLES, wav_data.params.framerate)
        _, end_sec = seconds_for_block(end_block, BLOCK_SAMPLES, wav_data.params.framerate)
        print(f"Possible modification detected near {fmt_time(start_sec)} - {fmt_time(end_sec)}")

    if Path(AUDIO_FILE).name == "tampered.wav":
        write_marker(".tamper_localized_done")
        mark_result("PASS_TAMPER_LOCALIZED")


if __name__ == "__main__":
    main()
