#!/usr/bin/env python3
import argparse

from self_marking import mark_result, read_wav, write_wav


def clamp_pcm16(value):
    return max(-32768, min(32767, value))


def main():
    parser = argparse.ArgumentParser(description="Modify a selected time range in a WAV file.")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--start", type=float, default=3.20)
    parser.add_argument("--end", type=float, default=3.80)
    parser.add_argument("--delta", type=int, default=1800)
    args = parser.parse_args()

    if args.end <= args.start:
        raise SystemExit("--end phai lon hon --start")

    wav_data = read_wav(args.input)
    rate = wav_data.params.framerate
    start = max(0, int(args.start * rate))
    end = min(len(wav_data.samples), int(args.end * rate))
    if start >= end:
        raise SystemExit("khoang sua nam ngoai file audio")

    for index in range(start, end):
        wavelet = args.delta if (index // 64) % 2 == 0 else -args.delta
        wav_data.samples[index] = clamp_pcm16(wav_data.samples[index] + wavelet)

    write_wav(args.output, wav_data)
    if args.output == "tampered.wav":
        mark_result("PASS_TAMPERED_CREATED")
    print(f"tampered={args.output}")
    print(f"range={args.start:.2f}-{args.end:.2f}s")


if __name__ == "__main__":
    main()
