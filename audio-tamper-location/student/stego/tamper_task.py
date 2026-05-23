#!/usr/bin/env python3
from self_marking import mark_result, read_wav, write_wav


AUDIO_FILE = ""
MESSAGE_FILE = ""
OUTPUT_FILE = "tampered.wav"
START_TIME = 3.20
END_TIME = 3.80


def clamp_pcm16(value):
    return max(-32768, min(32767, value))


def message_bytes(path):
    text = open(path, "r", encoding="utf-8").read().strip()
    if not text:
        raise ValueError(f"{path} rong")
    return text.encode("utf-8")


def main():
    if not AUDIO_FILE or not MESSAGE_FILE:
        raise SystemExit("Hay dien ten file vao cac dong TODO trong tamper_task.py")
    if END_TIME <= START_TIME:
        raise SystemExit("END_TIME phai lon hon START_TIME")

    payload = message_bytes(MESSAGE_FILE)
    wav_data = read_wav(AUDIO_FILE)
    rate = wav_data.params.framerate
    start = max(0, int(START_TIME * rate))
    end = min(len(wav_data.samples), int(END_TIME * rate))
    if start >= end:
        raise SystemExit("khoang sua nam ngoai file audio")

    for index in range(start, end):
        byte = payload[(index - start) % len(payload)]
        delta = 900 + (byte % 1200)
        wavelet = delta if (index // 64) % 2 == 0 else -delta
        wav_data.samples[index] = clamp_pcm16(wav_data.samples[index] + wavelet)

    write_wav(OUTPUT_FILE, wav_data)
    if OUTPUT_FILE == "tampered.wav":
        mark_result("PASS_TAMPERED_CREATED")
    print(f"tampered={OUTPUT_FILE}")


if __name__ == "__main__":
    main()
