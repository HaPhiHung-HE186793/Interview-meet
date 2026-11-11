# Interview-Meet Context Engine

**Thư ký Họp Tàng hình (`Bot-free`) + Bộ nhớ Ngữ cảnh Cá nhân chuẩn `MCP` + Huấn luyện viên Phỏng vấn Thích ứng (`Post-Call Debrief` & `Adaptive HR Coach`)** dành cho kỹ sư phần mềm, BA, PM và nhân sự làm việc song ngữ Anh–Việt.

---

## Kiến Trúc Cốt Lõi 5 Tầng

1. **Thu âm Tách 2 Kênh Không Dùng Bot (`Client-Side Web Audio`):** Tách độc lập luồng âm thanh Tab Google Meet (`getDisplayMedia`) và Micro cá nhân (`getUserMedia`), lưu nén cục bộ tại `IndexedDB` trình duyệt để bấm mốc giây nghe lại kiểm chứng (`Citation-backed Audio`) với chi phí lưu trữ đám mây `0đ`.
2. **Đường ống AI 2 Bước Tối ưu Chi phí & Code-Switching Anh–Việt:** Lọc khoảng lặng `VAD` $\rightarrow$ Gỡ băng bằng `Groq (whisper-large-v3-turbo)` / `Soniox` kèm từ điển thuật ngữ trích từ CV/JD $\rightarrow$ Hậu kiểm bằng `Gemini 2.5 Flash` (`Structured Outputs`).
3. **Bộ nhớ Cá nhân Lai 3 Bảng (`Neon PostgreSQL` + `pgvector`):** `sessions`, `qa_pairs`, `weakness_profile`.
4. **Cổng Kết nối Ngữ cảnh Cá nhân (`Python MCP Server` & `Context Pack`):** Kết nối trực tiếp vào Gemini CLI, VS Code, Antigravity IDE.
5. **Huấn luyện viên HR Thích ứng (`Error-Driven Loop`):** Đóng vai HR/Tech Lead hỏi biến tấu & xoáy sâu vào đúng các điểm yếu chưa khắc phục từ lịch sử phỏng vấn thật.

---

## Cấu Trúc Thư Mục

- [GEMINI.md](GEMINI.md): Bộ nhớ ngữ cảnh gốc & quy tắc kiến trúc của dự án.
- [docs/00_MASTER_SPEC.md](docs/00_MASTER_SPEC.md): Hồ sơ tổng hợp kiến trúc, kinh tế đơn vị vốn `0đ` và lộ trình PoC 14 ngày (4 Cổng Go/No-Go).
- [docs/01_MARKET_RESEARCH_Q4_2026.md](docs/01_MARKET_RESEARCH_Q4_2026.md): Báo cáo khảo sát Deep Research thị trường & đối thủ cạnh tranh Q4/2026.
- [docs/02_IDEATION_AND_WORKFLOW_GUIDE.md](docs/02_IDEATION_AND_WORKFLOW_GUIDE.md): Nhật ký ý tưởng gốc, chiến thuật sống còn vốn `0đ` và quy trình phối hợp Gemini Web – NotebookLM – Antigravity.
- [poc/gate1/](poc/gate1/README.md): **Cổng 1 (Ngày 1–3)** — Giao diện Web PoC thu âm tách 2 kênh lưu `IndexedDB` + Script Python benchmark STT song ngữ Anh–Việt.

---

## Chạy Nhanh Cổng 1 (Gate 1 PoC)

```bash
# 1. Mở giao diện thu âm tách 2 kênh tại http://localhost:8765
python3 -m http.server 8765 --directory poc/gate1

# 2. Cấu hình API Key
cp .env.example .env

# 3. Chạy benchmark gỡ băng 2 kênh Anh–Việt
python3 poc/gate1/benchmark_stt.py \
  --tab-audio ~/Downloads/<phien>_ch1_hr_tab.webm \
  --mic-audio ~/Downloads/<phien>_ch2_user_mic.webm
```
