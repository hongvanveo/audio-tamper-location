#!/usr/bin/env python3
import argparse
import math
from array import array

from self_marking import WavData, mark_result, write_wav


def main():
    parser = argparse.ArgumentParser(description="Generate a mono PCM16 WAV for the lab.")
    parser.add_argument("--out", default="cover.wav")
    parser.add_argument("--seconds", type=float, default=5.0)
    parser.add_argument("--rate", type=int, default=44100)
    args = parser.parse_args()

    samples = array("h")
    total = int(args.seconds * args.rate)
    for i in range(total):
        t = i / args.rate
        value = 0.40 * math.sin(2 * math.pi * 440 * t)
        value += 0.22 * math.sin(2 * math.pi * 660 * t)
        value += 0.10 * math.sin(2 * math.pi * 1230 * t)
        samples.append(int(value * 28000))

    params = (1, 2, args.rate, len(samples), "NONE", "not compressed")
    write_wav(args.out, WavData(params, samples))
    mark_result("PASS_COVER_CREATED")
    print(f"created={args.out}")


if __name__ == "__main__":
    main()
