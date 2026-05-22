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
mark_blocks.py
verify_blocks.py
tamper_audio.py
refresh_status.py
self_marking.py
```

## Mục tiêu bài lab

Sinh viên cần:

1. Tạo file audio gốc `cover.wav`.
2. Nhúng chữ ký self-marking theo từng block để tạo `marked.wav`.
3. Xác minh `marked.wav` chưa bị chỉnh sửa.
4. Tạo file `tampered.wav` bằng cách sửa một đoạn thời gian trong audio.
5. Chạy chương trình kiểm tra để phát hiện các block bị sửa.
6. Đọc kết quả khoanh vùng thời gian nghi ngờ.
7. Chạy `checkwork` để đạt đủ 6 mục `Y`.

## Nội dung kỹ thuật

Quy trình của lab:

```text
cover.wav
-> chia audio thành các block 1024 mẫu
-> tính SHA-256 rút gọn cho payload của từng block
-> nhúng chữ ký vào các bit LSB đầu block
-> tạo marked.wav
-> sửa một đoạn audio để tạo tampered.wav
-> đọc lại chữ ký và tính lại hash từng block
-> block nào sai hash thì báo TAMPERED
-> đổi vị trí block sang mốc thời gian
```

Ý nghĩa các khái niệm:

- `Self-marking`: file tự chứa thông tin kiểm tra của chính nó.
- `Fragile watermark`: watermark dễ bị hỏng khi file bị chỉnh sửa.
- `Block hash`: mỗi block có hash riêng để phát hiện vùng bị thay đổi.
- `Tamper localization`: xác định gần đúng vị trí hoặc khoảng thời gian bị sửa.
- `LSB`: bit ít quan trọng nhất của mẫu âm thanh, dùng để nhúng chữ ký nhỏ.

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

## Task 2: Nhúng chữ ký self-marking vào audio

Chạy:

```bash
python3 mark_blocks.py cover.wav marked.wav
```

Kết quả mẫu:

```text
tamper-location signature embedded.
blocks=215
output=marked.wav
```

Kiểm tra file:

```bash
ls -l marked.wav
```

## Task 3: Kiểm tra file marked.wav còn nguyên vẹn

Chạy:

```bash
python3 verify_blocks.py marked.wav
```

Nếu file chưa bị sửa, chương trình sẽ báo chữ ký được tìm thấy và các block đều `OK`.

Có thể dùng bản rút gọn để chỉ hiện phần quan trọng:

```bash
python3 verify_blocks.py marked.wav --quiet-ok
```

Kết quả mong đợi:

```text
tamper-location signature found.
No modification detected.
```

## Task 4: Tạo file audio bị chỉnh sửa

Lab có sẵn script `tamper_audio.py` để giả lập việc chỉnh sửa một đoạn audio.

Chạy:

```bash
python3 tamper_audio.py marked.wav tampered.wav --start 3.20 --end 3.80
```

Ý nghĩa:

- `marked.wav`: file đã có chữ ký self-marking.
- `tampered.wav`: file đầu ra sau khi bị sửa.
- `--start 3.20`: bắt đầu sửa tại giây 3.20.
- `--end 3.80`: kết thúc sửa tại giây 3.80.

Kết quả mẫu:

```text
tampered=tampered.wav
range=3.20-3.80s
```

Kiểm tra file:

```bash
ls -l tampered.wav
```

## Task 5: Phát hiện block bị chỉnh sửa

Chạy:

```bash
python3 verify_blocks.py tampered.wav
```

Hoặc dùng bản rút gọn:

```bash
python3 verify_blocks.py tampered.wav --quiet-ok
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
python3 mark_blocks.py cover.wav marked.wav
python3 verify_blocks.py marked.wav --quiet-ok
python3 tamper_audio.py marked.wav tampered.wav --start 3.20 --end 3.80
python3 verify_blocks.py tampered.wav --quiet-ok
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
