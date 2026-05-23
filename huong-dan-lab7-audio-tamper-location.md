# Hướng dẫn thực hành Lab 7: audio-tamper-location

Tài liệu này áp dụng cho:

- Lab 7: `audio-tamper-location`

## Lưu ý chung

- Bài lab dùng một container duy nhất.
- Sinh viên thao tác chính trong thư mục `~/stego`.
- Lab minh họa cơ chế fragile self-marking watermark cho audio WAV PCM16.
- File audio được chia thành nhiều block, mặc định 1024 mẫu mỗi block.
- Mỗi block tự chứa hash rút gọn của chính block đó.
- Khi một đoạn audio bị sửa, chương trình có thể phát hiện block nào bị thay đổi và suy ra khoảng thời gian nghi ngờ.
- Nếu sinh viên muốn làm lại từ đầu, dùng:

```bash
labtainer -r audio-tamper-location
```

## Tải bài lab

Trên máy Labtainer VM, mở terminal và gõ:

```bash
imodule https://raw.githubusercontent.com/hongvanveo/audio-tamper-location/main/imodule_audio-tamper-location.tar
```

## Khởi động bài lab

```bash
labtainer -r audio-tamper-location
```

Khi được hỏi email hoặc mã người học, sinh viên nhập mã sinh viên của mình, ví dụ:

```text
B22DCAT311
```

Sau khi khởi động xong, chuyển vào thư mục thực hành:

```bash
cd ~/stego
ls -l
```

Các file quan trọng:

```text
generate_cover.py
embed_task.py
verify_task.py
tamper_task.py
refresh_status.py
self_marking.py
```

## Mục tiêu bài lab

Sinh viên cần:

1. Tạo file audio gốc `cover.wav`.
2. Tạo file `sign.txt` chứa nội dung chữ ký.
3. Sửa file task để điền tên file audio và file chữ ký, sau đó tạo `marked.wav`.
4. Xác minh `marked.wav` chưa bị chỉnh sửa.
5. Tạo file `message.txt` để điều khiển nội dung chỉnh sửa audio.
6. Sửa file task để điền tên file message và file audio, sau đó tạo `tampered.wav`.
7. Chạy chương trình kiểm tra để phát hiện các block bị sửa.
8. Đọc kết quả khoanh vùng thời gian nghi ngờ.
9. Chạy `checkwork` để đạt đủ 6 mục `Y`.

## Nội dung kỹ thuật

Quy trình của lab:

```text
sign.txt + cover.wav
-> chia audio thành các block 1024 mẫu
-> tính hash cho payload của từng block co tron noi dung sign.txt
-> nhúng chữ ký vào các bit LSB đầu block
-> tạo marked.wav
-> message.txt + marked.wav
-> tạo sai lệch trên một khoảng thời gian audio
-> tạo tampered.wav
-> dùng lại sign.txt để tính lại hash từng block
-> block nào sai hash thì báo TAMPERED
-> đổi vị trí block sang mốc thời gian
```

Ý nghĩa các khái niệm:

- `Self-marking`: file tự chứa thông tin kiểm tra của chính nó.
- `Fragile watermark`: watermark dễ bị hỏng khi file bị chỉnh sửa.
- `Block hash`: mỗi block có hash riêng để phát hiện vùng bị thay đổi.
- `Tamper localization`: xác định gần đúng vị trí hoặc khoảng thời gian bị sửa.
- `LSB`: bit ít quan trọng nhất của mẫu âm thanh, dùng để nhúng chữ ký nhỏ.
- `sign.txt`: dữ liệu chữ ký do sinh viên tự tạo, được trộn vào quá trình ký từng block.
- `message.txt`: thông điệp do sinh viên tự tạo, dùng để tạo mẫu sai lệch khi chỉnh sửa audio.

## Task 1: Tạo file audio gốc

Trong terminal của lab:

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav --seconds 5
```

Kiểm tra file đã được tạo:

```bash
ls -l cover.wav
```

## Task 2: Tạo file sign.txt

Trong terminal của lab:

```bash
cd ~/stego
nano sign.txt
```

Sinh viên tự nhập một nội dung chữ ký, ví dụ:

```text
fragile audio signature
```

Lưu file rồi kiểm tra:

```bash
ls -l sign.txt
cat sign.txt
```

## Task 3: Sửa file task để nhúng chữ ký self-marking vào audio

Mở file:

```bash
nano embed_task.py
```

Trong file này, sửa hai dòng TODO:

```python
AUDIO_FILE = ""
SIGN_FILE = ""
```

thành:

```python
AUDIO_FILE = "cover.wav"
SIGN_FILE = "sign.txt"
```

Sau đó chạy:

```bash
python3 embed_task.py
ls -l marked.wav
```

## Task 4: Kiểm tra file marked.wav còn nguyên vẹn

Mở file:

```bash
nano verify_task.py
```

Trong file này, sửa hai dòng TODO:

```python
AUDIO_FILE = ""
SIGN_FILE = ""
```

thành:

```python
AUDIO_FILE = "marked.wav"
SIGN_FILE = "sign.txt"
```

Chạy:

```bash
python3 verify_task.py
```

Nếu file chưa bị sửa, chương trình sẽ báo chữ ký được tìm thấy và các block đều `OK`.

Kết quả mong đợi:

```text
tamper-location signature found.
No modification detected.
```

## Task 5: Tạo file message.txt

Trong terminal của lab:

```bash
cd ~/stego
nano message.txt
```

Sinh viên tự nhập một thông điệp, ví dụ:

```text
tamper this region
```

Kiểm tra file:

```bash
ls -l message.txt
cat message.txt
```

## Task 6: Sửa file task để tạo file audio bị chỉnh sửa

Mở file:

```bash
nano tamper_task.py
```

Trong file này, sửa hai dòng TODO:

```python
AUDIO_FILE = ""
MESSAGE_FILE = ""
```

thành:

```python
AUDIO_FILE = "marked.wav"
MESSAGE_FILE = "message.txt"
```

Sau đó chạy:

```bash
python3 tamper_task.py
ls -l tampered.wav
```

## Task 7: Phát hiện block bị chỉnh sửa

Mở lại file:

```bash
nano verify_task.py
```

Sửa hai dòng:

```python
AUDIO_FILE = "marked.wav"
SIGN_FILE = "sign.txt"
```

thành:

```python
AUDIO_FILE = "tampered.wav"
SIGN_FILE = "sign.txt"
```

Chạy:

```bash
python3 verify_task.py
```

Kết quả mẫu:

```text
tamper-location signature found.
Block 137: TAMPERED
Block 138: TAMPERED
Block 139: TAMPERED
...
Block 163: TAMPERED
Possible modification detected near 00:03.18 - 00:03.81
```

Khoảng thời gian có thể hơi rộng hơn đoạn sửa thật vì chương trình khoanh vùng theo biên block 1024 mẫu.

Sau khi hoàn thành tất cả các task, chạy `checkwork`:

```bash
checkwork audio-tamper-location
```

Kết quả đúng cuối cùng:

```text
Y - cover_created
Y - marked_created
Y - signature_found
Y - clean_audio_ok
Y - tampered_created
Y - tamper_localized
```

## Kiểm tra nhanh toàn bộ bài lab

Nếu cần chạy nhanh toàn bộ quy trình trong một lượt:

```bash
cd ~/stego
python3 generate_cover.py --out cover.wav --seconds 5
nano sign.txt
nano embed_task.py
python3 embed_task.py
nano verify_task.py
python3 verify_task.py
nano message.txt
nano tamper_task.py
python3 tamper_task.py
nano verify_task.py
python3 verify_task.py
checkwork audio-tamper-location
```

## Ý nghĩa các mục checkwork

- `cover_created`: đã tạo file audio gốc `cover.wav`.
- `marked_created`: đã tạo file `marked.wav` có chữ ký self-marking.
- `signature_found`: chương trình kiểm tra tìm thấy chữ ký trong `marked.wav`.
- `clean_audio_ok`: `marked.wav` được xác minh là chưa bị chỉnh sửa.
- `tampered_created`: đã tạo file `tampered.wav` bằng cách sửa một đoạn audio.
- `tamper_localized`: chương trình đã phát hiện và khoanh vùng block bị chỉnh sửa.

## Câu hỏi gợi ý cho báo cáo

1. Vì sao watermark trong bài lab được gọi là fragile watermark?
2. Vì sao chương trình có thể xác định gần đúng vị trí bị sửa thay vì chỉ báo file bị sửa?
3. Vì sao khoảng thời gian báo lỗi có thể rộng hơn đoạn sửa thật?
4. Nếu tăng kích thước block từ 1024 lên 4096 mẫu, khả năng khoanh vùng sẽ thay đổi thế nào?
5. Vì sao hash không được tính trực tiếp trên toàn bộ block sau khi nhúng chữ ký?

## Kết thúc bài lab

Trên terminal chính của Labtainer:

```bash
stoplab audio-tamper-location
```

Kết quả sẽ được lưu tại:

```bash
/home/student/labtainer_xfer/audio-tamper-location
```

Tên file bài làm có dạng:

```text
B22DCAT311.audio-tamper-location.lab
```
