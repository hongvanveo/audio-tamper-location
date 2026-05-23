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
printf 'my signature\n' > sign.txt
nano embed_task.py
python3 embed_task.py
nano verify_task.py
python3 verify_task.py
python3 verify_blocks.py marked.wav sign.txt
printf 'my tamper message\n' > message.txt
nano tamper_task.py
python3 tamper_task.py
nano verify_task.py
python3 verify_task.py
python3 verify_blocks.py tampered.wav sign.txt --changed-only
```

Trong `embed_task.py`, sinh vien dien ten file audio va file chu ky vao
hai dong TODO. Trong `tamper_task.py`, sinh vien dien ten file audio va
file message can dung de tao sai lech audio.

`verify_task.py` gio in day du trang thai tung block theo dang:

```text
tamper-location signature found.
Block 0: OK
Block 1: OK
Block 2: TAMPERED
Block 3: OK
```

Neu chi muon xem cac block bi sua va moc thoi gian nghi ngo, dung:

```bash
python3 verify_blocks.py tampered.wav sign.txt --changed-only
```

Ket qua mong doi khi verify file da bi sua:

```text
tamper-location signature found.
Block 137: TAMPERED
Block 138: TAMPERED
Possible modification detected near 00:03.20 - 00:03.80
```

Checkwork co 6 muc:

- `cover_created`
- `marked_created`
- `signature_found`
- `clean_audio_ok`
- `tampered_created`
- `tamper_localized`

