#!/usr/bin/env python3
import argparse
from pathlib import Path

from self_marking import (
    DEFAULT_BLOCK_SAMPLES,
    MAGIC,
    VERSION,
    digest_payload,
    ensure_block_size,
    extract_signature,
    fmt_time,
    full_block_count,
    mark_result,
    read_wav,
    seconds_for_block,
    write_marker,
)


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
    parser = argparse.ArgumentParser(description="Verify fragile tamper-location signatures in WAV blocks.")
    parser.add_argument("input")
    parser.add_argument("--block-samples", type=int, default=DEFAULT_BLOCK_SAMPLES)
    parser.add_argument("--quiet-ok", action="store_true", help="only print tampered blocks after the header")
    args = parser.parse_args()

    ensure_block_size(args.block_samples)
    wav_data = read_wav(args.input)
    count = full_block_count(wav_data.samples, args.block_samples)
    if count == 0:
        raise SystemExit("file qua ngan, khong du mot block")

    signatures = [
        extract_signature(wav_data.samples, block_index, args.block_samples)
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
        current_digest = digest_payload(wav_data.samples, block_index, args.block_samples)
        ok = magic == MAGIC and version == VERSION and embedded_digest == current_digest
        if ok:
            if not args.quiet_ok:
                print(f"Block {block_index}: OK")
        else:
            tampered.append(block_index)
            print(f"Block {block_index}: TAMPERED")

    if not tampered:
        print("No modification detected.")
        if Path(args.input).name == "marked.wav":
            write_marker(".clean_audio_ok_done")
            mark_result("PASS_CLEAN_AUDIO_OK")
        return

    for start_block, end_block in ranges(tampered):
        start_sec, _ = seconds_for_block(start_block, args.block_samples, wav_data.params.framerate)
        _, end_sec = seconds_for_block(end_block, args.block_samples, wav_data.params.framerate)
        print(
            "Possible modification detected near "
            f"{fmt_time(start_sec)} - {fmt_time(end_sec)}"
        )

    if Path(args.input).name == "tampered.wav":
        write_marker(".tamper_localized_done")
        mark_result("PASS_TAMPER_LOCALIZED")


if __name__ == "__main__":
    main()

