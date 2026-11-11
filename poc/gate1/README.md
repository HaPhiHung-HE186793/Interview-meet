# Cổng 1 (Ngày 1–3): Kiểm Chứng Thu Âm Tách 2 Kênh & Gỡ Băng Anh–Việt

Thư mục này chứa trọn bộ công cụ kiểm chứng giả định kỹ thuật rủi ro nhất của **Interview-Meet Context Engine** trước khi xây dựng Backend/Database.

---

## 1. Mở Trang Web PoC Thu Âm Tách 2 Kênh (`< 200 dòng`)

Trình duyệt Chrome yêu cầu ngữ cảnh bảo mật (`http://localhost`) để cấp quyền `getDisplayMedia` và `getUserMedia`. Chạy lệnh sau tại thư mục gốc dự án:

```bash
python3 -m http.server 8765 --directory poc/gate1
```

Sau đó mở **trình duyệt Google Chrome / Edge / Cốc Cốc bên ngoài** (không mở trong tab Preview nội bộ của IDE vì Electron WebView chặn `getDisplayMedia`) tại địa chỉ: **http://localhost:8765**

### Chế độ 1 — Test nhanh riêng Micro cá nhân (2 phút):
- Bấm **`🎤 Test Nhanh: Chỉ Thu Micro`** -> đọc đoạn kịch bản mẫu bên dưới -> bấm **`⏹ Dừng & Lưu IndexedDB`** -> tải file `.webm` Kênh 2 về chấm điểm `WER`.

### Chế độ 2 — Quy trình kiểm thử phòng họp Google Meet / YouTube tách 2 kênh:
1. Mở một phòng Google Meet ở tab bên cạnh (hoặc mở 1 video phỏng vấn kỹ thuật trên YouTube trong tab Chrome để giả lập giọng HR).
2. Quay sang tab `http://localhost:8765`, bấm **▶ Thu 2 Kênh (Meet + Micro)**.
3. Khi hộp thoại chia sẻ màn hình hiện lên:
   - Chọn tab **Thẻ Chrome (Chrome Tab)** đang mở Google Meet.
   - **Bắt buộc bật công tắc `"Chia sẻ cả âm thanh thẻ" (Also share tab audio)`** ở góc dưới hộp thoại.
4. Nói thử 3–5 phút theo đúng lối giao tiếp kỹ thuật song ngữ Anh–Việt (xem đoạn kịch bản mẫu bên dưới) ở cả 2 chế độ: **Đeo tai nghe** và **Bật loa ngoài**.
5. Bấm **⏹ Dừng & Lưu IndexedDB** -> Kiểm tra tính năng **🎯 Kiểm chứng nhảy mốc giây (Citation)** ngay trên giao diện rồi bấm **⬇ Tải Kênh 1 (`.webm`)** và **⬇ Tải Kênh 2 (`.webm`)**.

---

## 2. Chạy Script Đọ Sức STT (`Groq Whisper Large-v3-turbo` vs `Soniox`)

1. Tạo file `.env` ở thư mục gốc dự án và điền API key:
   ```bash
   cp .env.example .env
   ```
   - **Groq API Key (Miễn phí):** Tạo trong 30 giây tại https://console.groq.com/keys
   - **Soniox API Key (Tùy chọn đối chứng):** Tạo tại https://console.soniox.com

2. Chạy benchmark ghép 2 kênh độc lập (phân vai `[HR / Meet]` và `[Ứng viên]` chính xác 100% tốn `0đ`):
   ```bash
   python3 poc/gate1/benchmark_stt.py \
     --tab-audio ~/Downloads/ses_xxx_ch1_hr_tab.webm \
     --mic-audio ~/Downloads/ses_xxx_ch2_user_mic.webm \
     --vocab poc/gate1/sample_cv_jd_terms.json
   ```

3. *(Tùy chọn)* Đo tự động tỷ lệ lỗi từ (`WER %`) so với kịch bản chuẩn:
   ```bash
   python3 poc/gate1/benchmark_stt.py \
     --audio ~/Downloads/ses_xxx_ch2_user_mic.webm \
     --reference poc/gate1/sample_ground_truth.txt
   ```

---

## 3. Đoạn Kịch Bản Đọc Thử Code-Switching Anh–Việt (Test WER)

Bạn có thể đọc đoạn sau vào Micro để test độ nhạy bắt từ chuyên ngành của `Whisper Turbo` và `Soniox`:

> *"Trong dự án gần nhất, team mình chuyển từ kiến trúc monolith sang microservice và dùng PostgreSQL kết hợp pgvector để làm tìm kiếm ngữ nghĩa. Lúc tải cao khoảng 5.000 request mỗi giây, hệ thống từng dính lỗi deadlock và connection pool bị cạn khiến p99 latency vọt lên hơn 2 giây. Mình đã xử lý bằng cách đánh lại database indexing, thêm Redis cache kèm cơ chế rate limiting và đẩy các tác vụ nặng sang Kafka theo mô hình event-driven có đảm bảo idempotency."*

---

## 4. Tiêu Chuẩn Vượt Ải Cổng 1 (Go / No-Go Checklist)

- [ ] **Không lẫn kênh:** Kênh 1 chỉ chứa tiếng từ tab Google Meet, Kênh 2 chỉ chứa tiếng Micro của bạn (không bị echo khi đeo tai nghe).
- [ ] **Lưu & phát lại cục bộ:** F5 tải lại trang trình duyệt vẫn giữ nguyên các phiên ghi âm trong `IndexedDB`; nhập mốc giây bấm nghe lại nhảy đúng vị trí lệch `< 1 giây`.
- [ ] **Độ chuẩn Code-Switching Anh–Việt:** Các thuật ngữ trong `sample_cv_jd_terms.json` (*microservice, idempotency, pgvector, deadlock, throughput, p99 latency...*) được viết đúng tiếng Anh, không bị phiên âm méo sang tiếng Việt, `WER < 12%`.
- [ ] **Kinh tế đơn vị:** Chi phí quy đổi sau lọc khoảng lặng VAD nằm trong vùng mục tiêu `~600đ – 2.000đ / giờ họp`.
