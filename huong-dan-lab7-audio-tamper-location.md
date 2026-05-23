# Huong dan thuc hanh Lab 7: audio-tamper-location

Tai lieu nay ap dung cho:

- Lab 7: `audio-tamper-location`

## Luu y chung

- Bai lab dung mot container.
- Sinh vien thao tac trong thu muc `~/stego`.
- Lab minh hoa fragile self-marking watermark cho audio WAV PCM16.
- Audio duoc chia thanh nhieu block, mac dinh `1024` mau moi block.
- Moi block tu chua hash rut gon cua chinh block do.
- Khi mot doan audio bi sua, chuong trinh co the chi ra block nao bi thay doi va suy ra khoang thoi gian nghi ngo.

Neu can lam lai tu dau:

```bash
labtainer -r audio-tamper-location
```

## Tai bai lab

Tren may Labtainer VM:

```bash
imodule https://raw.githubusercontent.com/hongvanveo/audio-tamper-location/main/imodule_audio-tamper-location.tar
```

## Khoi dong bai lab

```bash
labtainer -r audio-tamper-location
```

Khi duoc hoi email hoac ma nguoi hoc, nhap ma sinh vien cua minh, vi du:

```text
B22DCAT311
```

Sau do vao thu muc thao tac:

```bash
cd ~/stego
ls -l
```

## Muc tieu bai lab

Sinh vien can:

1. Tao file audio goc `cover.wav`.
2. Tao file `sign.txt` chua chu ky.
3. Sua task de tao `marked.wav`.
4. Kiem tra `marked.wav` con nguyen ven.
5. Tao file `message.txt`.
6. Sua task de tao `tampered.wav`.
7. Kiem tra block nao bi sua.
8. Doc khoang thoi gian nghi ngo.
9. Chay `checkwork` va dat du 6 muc `Y`.

## Noi dung ky thuat

Quy trinh cua lab:

```text
sign.txt + cover.wav
-> chia audio thanh cac block 1024 mau
-> tinh hash cho payload cua tung block co tron noi dung sign.txt
-> nhung chu ky vao cac bit LSB dau block
-> tao marked.wav
-> message.txt + marked.wav
-> tao sai lech tren mot khoang thoi gian audio
-> tao tampered.wav
-> dung lai sign.txt de tinh lai hash tung block
-> block nao sai hash thi bao TAMPERED
-> doi vi tri block sang moc thoi gian
```

## Task 1: Tao file audio goc

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav --seconds 5
ls -l cover.wav
```

## Task 2: Tao file sign.txt

```bash
nano sign.txt
```

Nhap vi du:

```text
fragile audio signature
```

Kiem tra:

```bash
ls -l sign.txt
cat sign.txt
```

## Task 3: Tao marked.wav

Mo file:

```bash
nano embed_task.py
```

Sua hai dong:

```python
AUDIO_FILE = ""
SIGN_FILE = ""
```

thanh:

```python
AUDIO_FILE = "cover.wav"
SIGN_FILE = "sign.txt"
```

Chay:

```bash
python3 embed_task.py
ls -l marked.wav
```

## Task 4: Kiem tra marked.wav con nguyen ven

Mo file:

```bash
nano verify_task.py
```

Sua:

```python
AUDIO_FILE = ""
SIGN_FILE = ""
```

thanh:

```python
AUDIO_FILE = "marked.wav"
SIGN_FILE = "sign.txt"
```

Chay lenh in day du tat ca block:

```bash
python3 verify_task.py
```

Ket qua mong doi:

```text
tamper-location signature found.
Block 0: OK
Block 1: OK
Block 2: OK
Block 3: OK
...
No modification detected.
```

## Task 5: Tao file message.txt

```bash
nano message.txt
```

Nhap vi du:

```text
tamper this region
```

Kiem tra:

```bash
ls -l message.txt
cat message.txt
```

## Task 6: Tao file tampered.wav

Mo file:

```bash
nano tamper_task.py
```

Sua:

```python
AUDIO_FILE = ""
MESSAGE_FILE = ""
```

thanh:

```python
AUDIO_FILE = "marked.wav"
MESSAGE_FILE = "message.txt"
```

Chay:

```bash
python3 tamper_task.py
ls -l tampered.wav
```

## Task 7: Kiem tra file da bi sua

Mo lai:

```bash
nano verify_task.py
```

Sua:

```python
AUDIO_FILE = "marked.wav"
SIGN_FILE = "sign.txt"
```

thanh:

```python
AUDIO_FILE = "tampered.wav"
SIGN_FILE = "sign.txt"
```

### Cach 1: In day du tat ca block

```bash
python3 verify_task.py
```

Lenh nay in het cac block, block nao binh thuong thi hien `OK`, block nao bi sua thi hien `TAMPERED`.

Vi du:

```text
tamper-location signature found.
Block 0: OK
Block 1: OK
Block 2: OK
Block 3: OK
...
Block 137: TAMPERED
Block 138: TAMPERED
Block 139: TAMPERED
...
Possible modification detected near 00:03.18 - 00:03.81
```

### Cach 2: Chi in phan bi sua

```bash
python3 verify_blocks.py tampered.wav sign.txt --changed-only
```

Lenh nay chi in cac block bi sua va dong khoanh vung thoi gian nghi ngo.

Vi du:

```text
tamper-location signature found.
Block 137: TAMPERED
Block 138: TAMPERED
Block 139: TAMPERED
Possible modification detected near 00:03.18 - 00:03.81
```

Khoang thoi gian co the rong hon doan sua that vi chuong trinh khoanh vung theo bien block.

## Tom tat 2 lenh kiem tra

```bash
# In day du tat ca block
python3 verify_task.py

# Chi in cac block bi sua va khoang thoi gian nghi ngo
python3 verify_blocks.py tampered.wav sign.txt --changed-only
```

## Checkwork

Sau khi hoan thanh:

```bash
checkwork audio-tamper-location
```

Ket qua dung cuoi cung:

```text
Y - cover_created
Y - marked_created
Y - signature_found
Y - clean_audio_ok
Y - tampered_created
Y - tamper_localized
```

## Y nghia cac muc checkwork

- `cover_created`: da tao `cover.wav`.
- `marked_created`: da tao `marked.wav`.
- `signature_found`: tim thay chu ky self-marking.
- `clean_audio_ok`: `marked.wav` chua bi sua.
- `tampered_created`: da tao `tampered.wav`.
- `tamper_localized`: da phat hien va khoanh vung block bi sua.

## Ket thuc bai lab

```bash
stoplab audio-tamper-location
```

Ket qua se duoc luu tai:

```bash
/home/student/labtainer_xfer/audio-tamper-location
```
