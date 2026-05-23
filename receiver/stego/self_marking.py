#!/usr/bin/env python3
import hashlib
import os
import wave
from array import array
from pathlib import Path


MAGIC = b"SM"
VERSION = 1
DIGEST_BYTES = 5
SIGNATURE_BITS = (len(MAGIC) + 1 + DIGEST_BYTES) * 8
DEFAULT_BLOCK_SAMPLES = 1024
RESULT = Path.home() / ".local" / "result" / "tamper_location_check.txt"


class WavData:
    def __init__(self, params, samples):
        self.params = params
        self.samples = samples


def mark_result(token):
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    existing = RESULT.read_text(encoding="utf-8") if RESULT.exists() else ""
    if token not in existing:
        with RESULT.open("a", encoding="utf-8") as handle:
            handle.write(token + "\n")


def read_wav(path):
    with wave.open(str(path), "rb") as wav:
        params = wav.getparams()
        if params.nchannels != 1:
            raise ValueError("lab nay chi ho tro WAV mono")
        if params.sampwidth != 2:
            raise ValueError("lab nay chi ho tro WAV PCM16")
        samples = array("h")
        samples.frombytes(wav.readframes(params.nframes))
    return WavData(params, samples)


def write_wav(path, wav_data):
    with wave.open(str(path), "wb") as wav:
        wav.setparams(wav_data.params)
        wav.writeframes(wav_data.samples.tobytes())


def full_block_count(samples, block_samples):
    return len(samples) // block_samples


def block_bounds(block_index, block_samples):
    start = block_index * block_samples
    return start, start + block_samples


def digest_payload(samples, block_index, block_samples):
    start, end = block_bounds(block_index, block_samples)
    payload_start = start + SIGNATURE_BITS
    payload = samples[payload_start:end]
    data = payload.tobytes()
    return hashlib.sha256(data).digest()[:DIGEST_BYTES]


def load_text_bytes(path):
    data = Path(path).read_text(encoding="utf-8").strip()
    if not data:
        raise ValueError(f"{path} rong")
    return data.encode("utf-8")


def digest_payload_with_sign(samples, block_index, block_samples, sign_bytes):
    start, end = block_bounds(block_index, block_samples)
    payload_start = start + SIGNATURE_BITS
    payload = samples[payload_start:end]
    data = sign_bytes + b"\n" + payload.tobytes()
    return hashlib.sha256(data).digest()[:DIGEST_BYTES]


def bytes_to_bits(data):
    bits = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def bits_to_bytes(bits):
    out = bytearray()
    for offset in range(0, len(bits), 8):
        value = 0
        for bit in bits[offset:offset + 8]:
            value = (value << 1) | bit
        out.append(value)
    return bytes(out)


def signature_bytes(digest):
    return MAGIC + bytes([VERSION]) + digest


def embed_signature(samples, block_index, block_samples, signature):
    start, _ = block_bounds(block_index, block_samples)
    for offset, bit in enumerate(bytes_to_bits(signature)):
        sample = samples[start + offset]
        samples[start + offset] = (sample & ~1) | bit


def extract_signature(samples, block_index, block_samples):
    start, _ = block_bounds(block_index, block_samples)
    bits = [samples[start + offset] & 1 for offset in range(SIGNATURE_BITS)]
    raw = bits_to_bytes(bits)
    return raw[:2], raw[2], raw[3:]


def seconds_for_block(block_index, block_samples, rate):
    start = block_index * block_samples / rate
    end = (block_index + 1) * block_samples / rate
    return start, end


def fmt_time(seconds):
    minutes = int(seconds // 60)
    rem = seconds - minutes * 60
    return f"{minutes:02d}:{rem:05.2f}"


def write_marker(name):
    marker = Path.cwd() / name
    marker.write_text("done\n", encoding="utf-8")


def ensure_block_size(block_samples):
    if block_samples <= SIGNATURE_BITS:
        raise ValueError(f"block phai lon hon {SIGNATURE_BITS} mau")

