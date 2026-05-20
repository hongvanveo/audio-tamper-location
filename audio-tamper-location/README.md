# audio-tamper-location

Lab nay minh hoa co che fragile tamper-location watermark cho file WAV PCM16.
File audio tu chua thong tin kiem tra cua chinh no, va khi bi sua co the
khoanh vung block am thanh da thay doi.

Co che:

- Audio duoc chia thanh cac block mau, mac dinh 1024 mau moi block.
- Voi moi block, chuong trinh tinh SHA-256 rut gon tren phan payload cua block.
- Hash rut gon duoc nhung vao cac bit LSB dau block do.
- Khi xac minh, chuong trinh doc hash da nhung va tinh lai hash hien tai.
- Neu hai gia tri khac nhau, block do duoc bao la `TAMPERED`.

Cau truc minh hoa:

```text
BLOCK_0 | hash(BLOCK_0)
BLOCK_1 | hash(BLOCK_1)
BLOCK_2 | hash(BLOCK_2)
...
```

Trong hien thuc cua lab, hash duoc nhung vao chinh block bang LSB nen hash
chi tinh tren phan payload sau vung chua chu ky. Day la cach don gian de sinh
vien thay ro y tuong tamper-location ma khong can thu vien ngoai.

Luong thuc hanh:

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav --seconds 5
python3 mark_blocks.py cover.wav marked.wav
python3 verify_blocks.py marked.wav
python3 tamper_audio.py marked.wav tampered.wav --start 3.20 --end 3.80
python3 verify_blocks.py tampered.wav
```

Ket qua mong doi khi verify file da bi sua:

```text
tamper-location signature found.
Block 0: OK
Block 1: OK
Block 2: TAMPERED
Block 3: OK
Possible modification detected near 00:03.20 - 00:03.80
```

Checkwork co 6 muc:

- `cover_created`
- `marked_created`
- `signature_found`
- `clean_audio_ok`
- `tampered_created`
- `tamper_localized`

