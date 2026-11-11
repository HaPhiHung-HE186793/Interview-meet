# INTERVIEW-MEET CONTEXT ENGINE — MASTER PROJECT CONTEXT

**Định vị cốt lõi:** Thư ký Họp Tàng hình (`Bot-free`) + Bộ nhớ Ngữ cảnh Cá nhân chuẩn `MCP` + Huấn luyện viên Phỏng vấn Thích ứng (`Post-Call Debrief` & `Adaptive HR Coach`) tập trung vào kỹ sư phần mềm, BA, PM và nhân sự làm việc song ngữ Anh–Việt.

---

## 1. Bản Đồ Tài Liệu Nguồn (Knowledge Base)

Trước khi thiết kế tính năng, sửa schema database, chọn API, định giá hay thêm thư viện mới, luôn đối chiếu với các tài liệu gốc trong thư mục `docs/`:

- [docs/00_MASTER_SPEC.md](docs/00_MASTER_SPEC.md): Hồ sơ tổng hợp tầm nhìn sản phẩm, 4 hào lũy phòng thủ, kiến trúc 5 tầng, bài toán kinh tế đơn vị vốn `0đ` và lộ trình PoC 14 ngày (4 cổng Go/No-Go).
- [docs/01_MARKET_RESEARCH_Q4_2026.md](docs/01_MARKET_RESEARCH_Q4_2026.md): Báo cáo khảo sát Deep Research toàn cảnh thị trường & đối thủ Q4/2026 (bản đầy đủ số liệu Gartner, Greenhouse, Fabric, Stanford HAI, benchmark WER code-switching Anh–Việt, điểm yếu của Big Tech / Granola / Otter / nhóm Stealth Cheating / startup nội địa).
- [docs/02_IDEATION_AND_WORKFLOW_GUIDE.md](docs/02_IDEATION_AND_WORKFLOW_GUIDE.md): Nhật ký ý tưởng khởi nguồn, chiến thuật sống còn vốn `0đ`, nguyên tắc "3 Không" và quy trình phối hợp **Gemini Web + NotebookLM (`00_INTERVIEW_MEET_CONTEXT_ENGINE`) + Gem ↔ Antigravity IDE**.
- [docs/03_PROGRESS_AND_HOME_HANDOFF.md](docs/03_PROGRESS_AND_HOME_HANDOFF.md): Nhật ký tiến độ hiện tại (đã xong Pha 0 + Code & Lab Test Cổng 1 `WER = 1.39%`), hướng dẫn bàn giao thiết lập môi trường và kịch bản test giọng thật tại máy ở nhà để chuyển sang Cổng 2.

---

## 2. Kiến Trúc Kỹ Thuật 5 Tầng Đã Chốt

1. **Tầng 1 — Thu âm Tách 2 Kênh Không Dùng Bot (`Client-Side Web Audio`):**
   - `navigator.mediaDevices.getDisplayMedia({ audio: true, video: true })` bắt âm thanh tab Google Meet (**Kênh Đối tác / HR**).
   - `navigator.mediaDevices.getUserMedia({ audio: true })` bắt Micro cá nhân (**Kênh Người dùng**).
   - **Không trộn chung 2 kênh ngay từ đầu:** Giữ tách biệt để định danh người nói chính xác 100% với chi phí `Speaker Diarization = $0`.
   - Lọc khoảng lặng `VAD (Voice Activity Detection)` bằng WebAssembly ngay trên trình duyệt (cắt 25%–40% khoảng lặng) và lưu âm thanh nén (`WebM/Opus`) vào `IndexedDB` máy khách để bấm mốc giây nghe lại (`Citation-backed Audio`) tốn `$0` băng thông đám mây.

2. **Tầng 2 — Đường ống AI 2 Bước Tối ưu Chi phí & Code-Switching Anh–Việt:**
   - **Bước 2A (STT):** `Groq (whisper-large-v3-turbo)` hoặc `Soniox API`, truyền danh sách thuật ngữ chuyên ngành trích từ CV/JD vào `prompt`/`context` để bắt chuẩn câu nói pha trộn Anh–Việt kèm `timestamp` từng giây.
   - **Bước 2B (LLM Debrief):** Đẩy văn bản đã gỡ băng có gắn nhãn kênh và mốc giây sang `Gemini 2.5 Flash` / `Flash-Lite` với `Structured Outputs (JSON Schema)` để bóc tách quyết định họp, cặp Hỏi – Đáp, điểm `STAR`, lỗi diễn đạt và câu trả lời mẫu nâng cấp.

3. **Tầng 3 — Bộ nhớ Cá nhân Lai 3 Bảng (`Neon Serverless PostgreSQL` + `pgvector`):**
   - `sessions`: `id`, `user_id`, `session_type` (`meeting` | `interview` | `mock_hr`), `company_or_project`, `raw_transcript_json`, `summary_md`, `local_audio_ref`, `created_at`.
   - `qa_pairs`: `id`, `session_id`, `question_text`, `user_answer_text`, `audio_start_sec`, `audio_end_sec`, `star_score` (thang 10), `detected_flaws`, `upgraded_answer_sample`, `embedding` (`vector(768)` hoặc `vector(1536)`).
   - `weakness_profile`: `id`, `user_id`, `skill_topic`, `occurrence_count`, `avg_score`, `status` (`needs_work` | `practicing` | `mastered`), `last_tested_at`, `evidence_qa_ids`.

4. **Tầng 4 — Cổng Kết nối Ngữ cảnh Cá nhân (`Python MCP Server` & `Context Pack`):**
   - 3 công cụ MCP chuẩn: `search_meetings(query, date_range)`, `get_weak_topics(limit, status)`, `log_mock_practice_result(topic_id, new_score, notes)`.
   - Nút **Copy Context Pack** xuất hồ sơ năng lực & lịch sử liên quan thành Markdown tinh gọn để dán vào bất kỳ phiên chat AI nào trong 1 cú nhấp.

5. **Tầng 5 — Vòng lặp Huấn luyện viên HR Thích ứng (`Error-Driven Loop`):**
   - Nạp ngầm `weakness_profile` (`needs_work`) + nguyên văn `user_answer_text` cũ vào System Prompt của HR ảo -> hỏi biến tấu & xoáy sâu (`follow-up probe`) vào chỗ lấp lửng cũ -> chấm điểm đối chiếu **Hôm nay vs. Phỏng vấn thật** cho tới khi đạt ngưỡng chuyển sang `mastered`.

---

## 3. Lộ Trình Thực Thi PoC 14 Ngày (4 Cổng Go / No-Go)

- **Cổng 1 (Ngày 1–3):** HTML/JS cục bộ `< 200 dòng` tách 2 kênh lưu `IndexedDB` + Python script đo `Groq Whisper Large-v3-turbo` vs `Soniox` kèm từ khóa CV/JD. *Go khi: không lẫn kênh, không echo tai nghe, WER Anh–Việt `< 12%`, lệch timestamp `< 1s`.*
- **Cổng 2 (Ngày 4–7):** System Prompt `Gemini 2.5 Flash` xuất JSON chấm điểm `STAR` đối chiếu CV/JD + UI bấm nhận xét phát lại đúng giây audio gốc từ `IndexedDB`. *Go khi: `>= 80%` nhận xét trên 3 buổi thật chỉ trúng điểm mù khiến người nói tâm phục khẩu phục.*
- **Cổng 3 (Ngày 8–10):** Khởi tạo 3 bảng trên Neon Free Tier + Python MCP Server `~100 dòng`, tự làm "Khách hàng số 0" qua 3–5 buổi thực tế (`< 2s` truy vấn lỗi lặp lại).
- **Cổng 4 (Ngày 11–14):** Concierge MVP gắn Google Login của Neon + mã VietQR gói `99.000đ` ("Vé Săn Việc 30 Ngày") kiểm chứng với 10 ứng viên IT thật. *Go khi: tối thiểu 2–3 người chuyển khoản tiền thật.*

---

## 4. Quy Trình Đồng Bộ Giữa Gemini Web & Antigravity IDE

- **Gemini Web + Gem `Interview-Meet Partner & Architect` + Sổ NotebookLM `00_INTERVIEW_MEET_CONTEXT_ENGINE`:** Đóng vai trò Bộ não Nghiên cứu, khảo sát thị trường và phản biện kiến trúc.
- **Antigravity IDE (Repo `Interview-meet`):** Đóng vai trò Động cơ Thực thi Code, kiểm thử cục bộ và quản lý Git (`git@github.com:HaPhiHung-HE186793/Interview-meet.git` / https://github.com/HaPhiHung-HE186793/Interview-meet).
- **Quy tắc Git bắt buộc:** Mọi thay đổi code, cấu hình hoặc tài liệu sau khi hoàn thành và kiểm thử cục bộ đều phải được kiểm tra an toàn (`git status`, tuyệt đối không lọt `.env` hay file âm thanh thô), tạo commit rõ ràng và đẩy thẳng (`git push origin main` qua SSH) lên GitHub ngay.
- Mỗi khi có thay đổi kiến trúc hoặc kết quả thực nghiệm PoC quan trọng tại repo này, cập nhật lại `GEMINI.md` / `docs/` để đồng bộ ngược về sổ NotebookLM `00_INTERVIEW_MEET_CONTEXT_ENGINE`.
