#!/usr/bin/env python3
#!/usr/bin/env python3

raise SystemExit("Hay dung embed_task.py cho bai lab nay.")


def main():
    parser = argparse.ArgumentParser(description="Embed fragile tamper-location signatures into WAV blocks.")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--block-samples", type=int, default=DEFAULT_BLOCK_SAMPLES)
    args = parser.parse_args()

    ensure_block_size(args.block_samples)
    wav_data = read_wav(args.input)
    count = full_block_count(wav_data.samples, args.block_samples)
    if count == 0:
        raise SystemExit("file qua ngan, khong du mot block")

    for block_index in range(count):
        digest = digest_payload(wav_data.samples, block_index, args.block_samples)
        embed_signature(
            wav_data.samples,
            block_index,
            args.block_samples,
            signature_bytes(digest),
        )

    write_wav(args.output, wav_data)
    mark_result("PASS_MARKED_CREATED")
    print(f"tamper-location signature embedded.")
    print(f"blocks={count}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()

