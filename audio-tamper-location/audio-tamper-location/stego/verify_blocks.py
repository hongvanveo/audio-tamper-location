#!/usr/bin/env python3
import argparse

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
    read_wav,
    seconds_for_block,
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Xac minh tung block trong audio self-marking."
    )
    parser.add_argument("audio_file", help="Duong dan toi file WAV can kiem tra")
    parser.add_argument("sign_file", help="Duong dan toi file chu ky text")
    parser.add_argument(
        "--block-samples",
        type=int,
        default=DEFAULT_BLOCK_SAMPLES,
        help="So mau moi block, mac dinh 1024",
    )
    parser.add_argument(
        "--changed-only",
        action="store_true",
        help="Chi in cac block TAMPERED va khoang thoi gian nghi ngo",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ensure_block_size(args.block_samples)
    sign_bytes = load_text_bytes(args.sign_file)
    wav_data = read_wav(args.audio_file)
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

    tampered = []
    for block_index in range(count):
        magic, version, embedded_digest = signatures[block_index]
        current_digest = digest_payload_with_sign(
            wav_data.samples,
            block_index,
            args.block_samples,
            sign_bytes,
        )
        ok = magic == MAGIC and version == VERSION and embedded_digest == current_digest
        if ok:
            if not args.changed_only:
                print(f"Block {block_index}: OK")
        else:
            tampered.append(block_index)
            print(f"Block {block_index}: TAMPERED")

    if not tampered:
        print("No modification detected.")
        return

    for start_block, end_block in ranges(tampered):
        start_sec, _ = seconds_for_block(
            start_block, args.block_samples, wav_data.params.framerate
        )
        _, end_sec = seconds_for_block(
            end_block, args.block_samples, wav_data.params.framerate
        )
        print(f"Possible modification detected near {fmt_time(start_sec)} - {fmt_time(end_sec)}")


if __name__ == "__main__":
    main()

