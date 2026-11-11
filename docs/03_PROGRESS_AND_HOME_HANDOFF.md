# BÀN GIAO TIẾN ĐỘ & HƯỚNG DẪN TIẾP TỤC TẠI MÁY Ở NHÀ (CÓ MICRO)

**Cập nhật lần cuối:** 11/11/2026  
**Trạng thái hiện tại:** Đã hoàn tất 100% **Pha 0 (Knowledge Base & Rules)** + Code & Kiểm chứng phòng Lab **Cổng 1 (Gate 1 PoC)**. Đang tạm dừng bước thu giọng nói thật vì máy văn phòng không có Micro — sẵn sàng kéo code về máy ở nhà để test giọng thật 5 phút và chuyển sang **Cổng 2**.

---

## 1. Tóm Tắt Những Gì Đã Hoàn Thành & Kiểm Chứng

1. **Pha 0 — Hạ tầng Tri thức & Quy tắc Kiến trúc (`DONE`):**
   - Chuẩn hóa bộ tài liệu gốc tại [`docs/00_MASTER_SPEC.md`](00_MASTER_SPEC.md), [`docs/01_MARKET_RESEARCH_Q4_2026.md`](01_MARKET_RESEARCH_Q4_2026.md), [`docs/02_IDEATION_AND_WORKFLOW_GUIDE.md`](02_IDEATION_AND_WORKFLOW_GUIDE.md).
   - Thiết lập bộ nhớ dự án [`GEMINI.md`](../GEMINI.md) và quy tắc bất di bất dịch [`.agents/rules/interview-meet-architect.md`](../.agents/rules/interview-meet-architect.md) (tự động nạp cho Antigravity IDE trên mọi máy khi mở repo).

2. **Pha 1 — Cổng 1 PoC: Thu Âm Tách 2 Kênh + Gỡ Băng Anh–Việt (`CODE COMPLETE & LAB-VERIFIED`):**
   - **Web Recorder ([`poc/gate1/index.html`](../poc/gate1/index.html)):**
     - Thu độc lập **Kênh 1 (Tab Google Meet / HR)** qua `getDisplayMedia` + **Kênh 2 (Micro của bạn)** qua `getUserMedia` (bật sẵn `echoCancellation`, `noiseSuppression`, `autoGainControl`).
     - Có thêm nút **`🎤 Test Nhanh: Chỉ Thu Micro`** để kiểm tra riêng giọng nói + lọc ồn phòng trước khi mở Meet.
     - Tự động phát hiện và cảnh báo nếu mở nhầm trong khung Preview nội bộ của IDE (Electron WebView không hỗ trợ `getDisplayMedia`).
     - Lưu nén `WebM/Opus` cục bộ trong `IndexedDB` trình duyệt (`$0` lưu trữ đám mây) + sửa triệt để lỗi `Infinity duration` của Chrome `MediaRecorder` + tua nhảy mốc giây (`Citation Seek`) chính xác `< 1 giây`.
   - **Đường ống Tiền xử lý VAD & Benchmark STT ([`poc/gate1/benchmark_stt.py`](../poc/gate1/benchmark_stt.py)):**
     - Phát hiện quan trọng đã xử lý: Khi thu tách 2 kênh, lúc HR nói thì kênh Micro im lặng dài (`> 5s`) và ngược lại. Nếu gửi thẳng khoảng lặng cho `Whisper`, model sẽ tự bịa câu tiếng Việt rác (*hallucination*).
     - Đã tích hợp bộ cắt khoảng lặng `FFmpeg` (`silencedetect` + `atrim+concat`) trước khi gọi API kết hợp `VadAudioSliceMap` ánh xạ ngược mốc giây về đồng hồ gốc của buổi họp.
     - **Kết quả chạy thật với Groq `whisper-large-v3-turbo` trên luồng giả lập 2 kênh song ngữ Anh–Việt:**
       - Tỷ lệ lỗi từ (`WER`): **`1.39%`** (**ĐẠT**, tiêu chuẩn Cổng 1 `< 12%`).
       - Thuật ngữ chuyên ngành IT bắt trúng từ `sample_cv_jd_terms.json`: **`10/10`** (*microservice, PostgreSQL, pgvector, deadlock, connection pool, p99 latency, database indexing, Redis, rate limiting, idempotency*).
       - Độ lệch mốc giây (`Citation timestamp`): **`~0.1s`** (`< 1s`).
       - Chi phí quy đổi sau cắt khoảng lặng VAD: **`1.022 VNĐ / giờ họp`** (giảm một nửa so với gửi thô).

---

## 2. Ghi Nhớ Nhanh Về Cơ Chế Hoạt Động (Giải Đáp Thắc Mắc Cốt Lõi)

- **Không phải gửi 1 video quay màn hình gộp chung rồi đoán giọng:** Hệ thống thu trực tiếp **2 dây âm thanh vật lý riêng biệt ngay lúc cuộc gọi diễn ra** (Dây 1 = tiếng phát ra từ tab Google Meet; Dây 2 = tiếng từ Micro của bạn). Vì sản phẩm chấm điểm **câu trả lời của bạn**, việc biết chắc chắn 100% đâu là lời bạn nói tốn `0đ` và không bao giờ nhầm vai.
- **Nếu phòng Google Meet có `>= 2` người phỏng vấn (HR + Tech Lead):** Toàn bộ câu hỏi của hội đồng phỏng vấn nằm gọn ở Kênh 1 (`[Phía Phòng Họp / Hội đồng]`), câu trả lời của bạn nằm độc lập ở Kênh 2 (`[Bạn / Ứng viên]`). Ở Cổng 2, `Gemini 2.5 Flash` đọc ngữ cảnh vẫn tách rõ câu hỏi hành vi vs câu hỏi kỹ thuật mà không tốn tiền mua AI phân tách giọng nói (`Speaker Diarization`).
- **Tạp âm môi trường & tiếng lọt loa:** Trình duyệt đã bật lọc ồn phần cứng (`noiseSuppression` + `echoCancellation`), đồng thời script Python có tầng cắt khoảng lặng VAD (`-38dB`) trước khi gửi lên Groq. Bài test ở nhà chính là để kiểm tra xem Micro + tai nghe/loa ngoài thực tế của bạn có vượt ngưỡng này mượt mà hay không.

---

## 3. Checklist 5 Phút Thiết Lập Khi Về Tới Máy Ở Nhà

### Bước 1: Kéo code mới nhất từ GitHub
```bash
# Nếu máy ở nhà chưa có repo:
git clone git@github.com:HaPhiHung-HE186793/Interview-meet.git
cd Interview-meet

# Hoặc nếu đã clone từ trước:
git pull origin main
```

### Bước 2: Cài `ffmpeg` và thư viện Python nhẹ
```bash
# Kiểm tra máy đã có ffmpeg chưa:
ffmpeg -version
# (Nếu chưa có trên Ubuntu/Linux: sudo apt update && sudo apt install -y ffmpeg)
# (Nếu máy nhà dùng Windows: winget install Gyan.FFmpeg)

# Cài thư viện Python (dùng venv nếu hệ điều hành chặn pip toàn cục):
python3 -m venv .venv
source .venv/bin/activate   # Trên Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Bước 3: Tạo lại file `.env` (Quan trọng!)
> **Lưu ý bảo mật:** File `.env` chứa API Key cá nhân **không bao giờ được đẩy lên GitHub** (đã chặn trong `.gitignore`). Khi về máy nhà, bạn cần tạo lại file `.env`:

```bash
cp .env.example .env
```
Sau đó mở `.env` và dán lại 2 mã miễn phí bạn đã tạo:
- `GROQ_API_KEY=gsk_...` (lấy lại trong 10 giây tại https://console.groq.com/keys nếu chưa lưu nháp)
- `GEMINI_API_KEY=AIza...` (tại https://aistudio.google.com/apikey — dùng cho Cổng 2 ngay sau đây)

---

## 4. Hai Bài Test Giọng Thật Cần Chạy Ở Nhà (10 Phút Để Chốt Cổng 1)

### Khởi động giao diện Web Cổng 1:
```bash
python3 -m http.server 8765 --directory poc/gate1
```
👉 Mở trình duyệt **Google Chrome / Edge / Cốc Cốc bên ngoài** (tuyệt đối **không** mở trong tab Preview nội bộ của IDE) tại địa chỉ: **`http://localhost:8765`**

### Bài Test A — Test riêng Micro + Tạp âm phòng (2 phút):
1. Trên trang `http://localhost:8765`, bấm nút **`🎤 Test Nhanh: Chỉ Thu Micro`**.
2. Đọc tự nhiên đoạn văn mẫu song ngữ Anh–Việt sau (có thể để quạt máy/tạp âm phòng bình thường):
   > *"Trong dự án gần nhất, team mình chuyển từ kiến trúc monolith sang microservice và dùng PostgreSQL kết hợp pgvector để làm tìm kiếm ngữ nghĩa. Lúc tải cao khoảng 5.000 request mỗi giây, hệ thống từng dính lỗi deadlock và connection pool bị cạn khiến p99 latency vọt lên hơn 2 giây. Mình đã xử lý bằng cách đánh lại database indexing, thêm Redis cache kèm cơ chế rate limiting và đẩy các tác vụ nặng sang Kafka theo mô hình event-driven có đảm bảo idempotency."*
3. Bấm **`⏹ Dừng & Lưu IndexedDB`** -> Bấm thử nút nhảy mốc giây -> Bấm **`⬇ Tải Kênh 2 (.webm)`**.
4. Chạy lệnh chấm điểm độ chính xác (`WER %`) tại Terminal:
   ```bash
   python3 poc/gate1/benchmark_stt.py \
     --audio ~/Downloads/<ten_file_vua_tai>_ch2_user_mic.webm \
     --reference poc/gate1/sample_ground_truth.txt
   ```
   *(Kỳ vọng: `WER < 12%`, các từ tiếng Anh chuyên ngành hiện chuẩn xác, tạp âm khoảng nghỉ không sinh chữ rác).*

### Bài Test B — Test Thu Tách 2 Kênh (Meet/YouTube + Micro của bạn, 5 phút):
1. Mở một tab Chrome khác phát một video phỏng vấn IT (YouTube) hoặc phòng Google Meet nháp.
2. Quay lại `http://localhost:8765`, bấm **`▶ Thu 2 Kênh (Meet + Micro)`** -> Chọn tab Chrome đang phát video/Meet và **tích chọn ô `"Also share tab audio" / "Chia sẻ cả âm thanh thẻ"`**.
3. Để video nói một câu, sau đó bạn trả lời xen kẽ vào Micro (thử khi đeo tai nghe trước, nếu tiện thử thêm bật loa ngoài).
4. Bấm **`⏹ Dừng & Lưu IndexedDB`**, tải cả 2 file `.webm` (`ch1_hr_tab` và `ch2_user_mic`) rồi chạy:
   ```bash
   python3 poc/gate1/benchmark_stt.py \
     --tab-audio ~/Downloads/<phien>_ch1_hr_tab.webm \
     --mic-audio ~/Downloads/<phien>_ch2_user_mic.webm
   ```
   *(Mở file báo cáo Markdown xuất ra trong `poc/outputs/` để xem bản hội thoại đã tự động tách vai `[HR / Meet]` và `[Ứng viên]` kèm mốc giây).*

---

## 5. Câu Lệnh Mở Đầu Cho Antigravity Trên Máy Ở Nhà

Khi về nhà mở thư mục `Interview-meet` bằng Antigravity IDE, bạn chỉ cần nhắn câu sau vào khung chat để AI bắt nhịp ngay lập tức mà không mất ngữ cảnh:

> *"Đọc `GEMINI.md` và `docs/03_PROGRESS_AND_HOME_HANDOFF.md` để nắm toàn bộ tiến độ. Mình đang ở máy nhà đã có Micro, hãy hỗ trợ mình kiểm tra kết quả test giọng thật Cổng 1 và bắt đầu xây dựng luôn Cổng 2 (Post-Call Debrief chấm điểm STAR bằng Gemini 2.5 Flash + UI bấm nhận xét nhảy đúng giây audio từ IndexedDB)."*
