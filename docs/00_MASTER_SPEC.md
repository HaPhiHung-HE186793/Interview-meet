# HỒ SƠ TỔNG HỢP DỰ ÁN: INTERVIEW-MEET CONTEXT ENGINE
**Định vị cốt lõi:** Thư ký Họp Tàng hình (Bot-free) + Bộ nhớ Ngữ cảnh Cá nhân chuẩn MCP + Huấn luyện viên Phỏng vấn Thích ứng (Post-Call Debrief & Adaptive HR Coach) cho kỹ sư IT và nhân sự làm việc song ngữ Anh–Việt.

---

## 1. TẦM NHÌN SẢN PHẨM & BÀI TOÁN GIẢI QUYẾT

Sản phẩm không dừng lại ở công cụ ghi chú cuộc họp thông thường mà giải quyết trọn vẹn vòng lặp **Thu thập $\rightarrow$ Phân tích lỗ hổng $\rightarrow$ Lưu trữ ký ức dài hạn $\rightarrow$ Tái sử dụng ngữ cảnh & Luyện tập đối kháng**:

1. **Khi họp & phỏng vấn qua Google Meet:** Thu âm tách riêng 2 luồng âm thanh (giọng người dùng và giọng đối phương) trực tiếp trên trình duyệt mà **không cho Bot lạ nhảy vào phòng họp**, tránh gây phản cảm với HR/khách hàng và vượt qua rào cản không có quyền Host ghi hình.
2. **Sau buổi phỏng vấn / họp (Post-Call Debrief):** Bóc tách từng cặp Hỏi – Đáp, chấm điểm theo khung STAR đối chiếu với CV/JD, chỉ rõ câu trả lời vòng vo hoặc thiếu dẫn chứng kèm **mốc thời gian phát lại đúng đoạn âm thanh gốc** để tự kiểm chứng 100%.
3. **Bộ nhớ Ngữ cảnh Cá nhân (Personal Context Engine):** Tích lũy toàn bộ lịch sử họp và hồ sơ điểm yếu cá nhân vào cơ sở dữ liệu lai (`PostgreSQL` + `pgvector`), xuất trực tiếp qua **MCP Server** hoặc **Gói Context (Context Pack)** để Gemini, VS Code, Antigravity truy xuất tức thì.
4. **Huấn luyện viên HR Thích ứng (Error-Driven Loop):** Đóng vai HR/Tech Lead lấy đúng các câu hỏi người dùng từng trả lời kém trong quá khứ để hỏi biến tấu, xoáy sâu (follow-up probe), đối chiếu câu trả lời mới so với câu trả lời cũ cho đến khi khắc phục triệt để.

---

## 2. PHÂN TÍCH ĐỐI THỦ CẠNH TRANH & KHOẢNG TRỐNG THỊ TRƯỜNG (2025–2026)

### 2.1. Ma trận đối chiếu các nhóm đối thủ hiện hữu

| Nhóm đối thủ | Đại diện tiêu biểu | Mức giá tham khảo | Điểm yếu chí mạng & Khoảng trống bỏ ngỏ | Cơ sở để sản phẩm của chúng ta chiến thắng |
|---|---|---|---|---|
| **Big Tech Tích hợp sẵn** | Google Meet Gemini, MS Teams Copilot | Gói doanh nghiệp ($14–$30+/user/tháng) | **Quyền ghi chú thuộc về Host công ty tuyển dụng**, ứng viên khách mời bên ngoài không lấy được biên bản; không có bộ nhớ xuyên suốt nhiều công ty; nhận diện chêm từ chuyên ngành Anh–Việt kém. | Quyền sở hữu dữ liệu thuộc về **cá nhân ứng viên** bất kể ai là Host; bộ nhớ tích lũy xuyên suốt toàn bộ sự nghiệp. |
| **Ghi chú Bot-free Quốc tế** | Granola, Limitless | ~$18–$20/tháng (Thẻ quốc tế, thuê bao tự động) | Granola **xóa âm thanh gốc sau khi gỡ băng** nên không thể bấm nghe lại đoạn ấp úng để sửa lỗi giao tiếp; không có chế độ chấm điểm phỏng vấn đối kháng; giá cao với cá nhân VN. | Có **Citation-backed Audio** lưu cục bộ trình duyệt để nghe lại đúng giây bị vấp; có vòng lặp luyện HR ảo; bán gói ngắn hạn qua VietQR. |
| **Bot Họp Truyền thống** | Otter.ai, Fireflies.ai, Read.ai | $10–$39/tháng | Cho **Bot tự động xin vào phòng Meet** gây mất thiện cảm ngay lập tức khi đi phỏng vấn; từng dính làn sóng cấm đoán từ IT và kiện tụng vì tự ý gửi mail quảng cáo cho khách họp. | **100% Bot-free** qua Web Audio API; dữ liệu khép kín riêng tư, không tự phát tán email. |
| **Tool Nhắc bài Gian lận (Stealth Cheating)** | LockedIn AI, Final Round AI, Cluely | Rất đắt ($50–$149/tháng) | Tỷ lệ hủy gói cực cao sau 1 tháng; bị các hệ thống tuyển dụng phát hiện qua ánh mắt đọc chữ, độ trễ phản hồi và phím tắt; rủi ro đạo đức & pháp lý, mất cửa hợp tác B2B2C. | Định vị minh bạch: **Giải phẫu hậu kiểm (Debrief) & Luyện phản xạ trước giờ G**, tạo năng lực thật và mở rộng được với trường ĐH/trung tâm đào tạo. |
| **Công cụ Gỡ băng Nội địa VN** | Các giải pháp họp B2B/Chính phủ trong nước | Hợp đồng B2B lớn | Tập trung văn bản hành chính thuần Việt, thiếu tối ưu cho lối nói **code-switching Anh–Việt** của ngành IT/Product; không mở cổng MCP cá nhân cho lập trình viên. | Tối ưu từ điển chuyên ngành IT Anh–Việt từ CV/JD; mở sẵn chuẩn MCP cho hệ sinh thái AI cá nhân. |

### 2.2. Bốn Hào lũy Phòng thủ (Moats) chống đối thủ Clone trong 48 giờ

1. **Chi phí chuyển đổi tích lũy (Compounding Switching Cost):** Đối thủ copy được giao diện trong 2 ngày nhưng không thể copy biểu đồ tiến bộ kỹ năng và lịch sử họp/phỏng vấn kéo dài nhiều tháng của người dùng. Rời bỏ công cụ đồng nghĩa mất toàn bộ "trí nhớ sự nghiệp".
2. **Ngách chuyên môn dọc (Vertical AI cho IT/Tech song ngữ Anh–Việt):** Nạp tự động thuật ngữ từ CV, JD và tài liệu dự án vào pipeline gỡ băng, kết hợp bộ tiêu chí chấm điểm (Rubric) sát thực tế phỏng vấn Kỹ sư phần mềm, BA, PM, System Design.
3. **Kiến trúc Niềm tin & Kiểm chứng (Citation-backed Trust):** Mọi nhận xét của AI đều gắn mốc thời gian trỏ thẳng về đoạn âm thanh gốc lưu cục bộ trên máy người dùng, triệt tiêu nỗi sợ AI "bịa đặt" (hallucination) và bảo vệ tuyệt đối bí mật công việc.
4. **Cắm rễ vào quy trình làm việc qua MCP & Tối ưu Kinh tế Đơn vị:** Kết nối trực tiếp vào IDE/CLI hằng ngày qua chuẩn MCP và giữ chi phí xử lý cực thấp để các bản clone làm ẩu đẩy thẳng audio vào LLM đắt tiền tự thua lỗ khi phá giá.

---

## 3. KIẾN TRÚC KỸ THUẬT 5 TẦNG CỐT LÕI

### Tầng 1: Thu âm Tách 2 Kênh Không Dùng Bot (Client-Side Web Audio)
* Sử dụng `navigator.mediaDevices.getDisplayMedia({ audio: true, video: true })` để bắt luồng âm thanh phát ra từ tab Google Meet (Kênh Đối tác/HR) và `navigator.mediaDevices.getUserMedia({ audio: true })` để bắt Micro cá nhân (Kênh Người dùng).
* **Không trộn chung âm thanh ngay lập tức:** Giữ tách biệt 2 kênh để định danh người nói chính xác 100% với chi phí Speaker Diarization bằng $0.
* Tích hợp bộ lọc khoảng lặng **VAD (Voice Activity Detection)** bằng WebAssembly ngay trên trình duyệt để cắt bỏ 25%–40% thời gian im lặng trước khi gửi đi xử lý.
* Lưu tệp âm thanh nén (`WebM/Opus`) trực tiếp vào `IndexedDB` trên trình duyệt của người dùng để phục vụ tính năng bấm mốc giây nghe lại mà không tốn băng thông đám mây.

### Tầng 2: Đường ống AI 2 Bước Tối ưu Chi phí & Code-Switching Anh–Việt
* **Bước 2A – Speech-to-Text (STT):** Sử dụng `Groq (whisper-large-v3-turbo)` hoặc `Soniox API`. Truyền danh sách từ khóa chuyên ngành trích xuất từ CV/JD (ví dụ: *microservice, idempotency, pgvector, sprint backlog, latency*) vào tham số ngữ cảnh (`prompt` / `context`) để bắt chuẩn câu nói pha trộn tiếng Việt và tiếng Anh kèm timestamp chi tiết.
* **Bước 2B – Phân tích Hậu kiểm (LLM):** Đẩy văn bản đã gỡ băng có gắn nhãn kênh và mốc giây sang `Gemini 2.5 Flash` (hoặc `Flash-Lite`) với `Structured Outputs (JSON Schema)` để trích xuất quyết định cuộc họp, cặp câu hỏi – trả lời, điểm STAR, lỗi diễn đạt và gợi ý câu trả lời nâng cấp.

### Tầng 3: Bộ nhớ Cá nhân Lai 3 Bảng (`PostgreSQL` + `pgvector`)
Triển khai trên Neon (Serverless Postgres) gồm 3 bảng cốt lõi:
1. **`sessions` (Tầng Sự kiện thô):** `id`, `user_id`, `session_type` (`meeting` | `interview` | `mock_hr`), `company_or_project`, `raw_transcript_json`, `summary_md`, `local_audio_ref`, `created_at`.
2. **`qa_pairs` (Tầng Hỏi – Đáp & Đánh giá):** `id`, `session_id`, `question_text`, `user_answer_text`, `audio_start_sec`, `audio_end_sec`, `star_score` (thang 10), `detected_flaws` (mảng thẻ lỗi), `upgraded_answer_sample`, `embedding` (`vector(768)` hoặc `vector(1536)`).
3. **`weakness_profile` (Tầng Hồ sơ Năng lực Động):** `id`, `user_id`, `skill_topic`, `occurrence_count`, `avg_score`, `status` (`needs_work` | `practicing` | `mastered`), `last_tested_at`, `evidence_qa_ids`.

### Tầng 4: Cổng Kết nối Ngữ cảnh Cá nhân (MCP Server & Context Pack)
* Xây dựng **Python MCP Server** cung cấp các công cụ tiêu chuẩn:
  * `search_meetings(query, date_range)`: Tìm kiếm ngữ nghĩa kết hợp lọc thời gian các quyết định trong cuộc họp.
  * `get_weak_topics(limit, status)`: Lấy danh sách các điểm yếu chưa khắc phục kèm câu trả lời lỗi thực tế.
  * `log_mock_practice_result(topic_id, new_score, notes)`: Cập nhật tiến bộ sau phiên luyện tập.
* Nút **"Xuất Gói Ngữ Cảnh (Copy Context Pack)"** trên Web App cho phép đóng gói hồ sơ năng lực và lịch sử liên quan thành Markdown tinh gọn trong 1 cú nhấp chuột để dán vào phiên chat Gemini Web bất kỳ.

### Tầng 5: Vòng lặp Huấn luyện viên HR Thích ứng (Adaptive HR Loop)
* Nạp ngầm `weakness_profile` có trạng thái `needs_work` cùng nguyên văn `user_answer_text` cũ vào System Prompt của HR ảo.
* Biến tấu câu hỏi và tung câu hỏi xoáy (follow-up) đúng vào chi tiết lần trước ứng viên trả lời lấp lửng.
* Chấm điểm đối chiếu trực tiếp **Câu trả lời hôm nay vs. Câu trả lời hôm phỏng vấn thật**, yêu cầu nói lại phần còn thiếu cho đến khi đạt ngưỡng điểm mới chuyển sang trạng thái `mastered`.

---

## 4. BÀI TOÁN CHI PHÍ (UNIT ECONOMICS) & CHIẾN LƯỢC SỐNG CÒN VỐN 0 ĐỒNG

### 4.1. Bảng định mức chi phí hạ tầng & API (Tỷ giá quy chiếu: $1 \text{ USD} \approx 25.500 \text{ VNĐ}$)

| Thành phần | Lựa chọn tối ưu | Hạn mức Miễn phí (Free Tier) | Đơn giá khi mở rộng trả phí |
|---|---|---|---|
| **Gỡ băng STT** | Groq `whisper-large-v3-turbo` | Miễn phí hạn mức dev hằng ngày | $\$0.04/\text{giờ}$ ($\sim 1.020\text{đ}/\text{giờ}$); Batch không đồng bộ chỉ $\$0.02/\text{giờ}$ ($\sim 510\text{đ}/\text{giờ}$) |
| **Phân tích & Chấm điểm LLM** | `Gemini 2.5 Flash` / `Flash-Lite` | Miễn phí 500–1.500 request/ngày trên AI Studio | $\$0.10 - \$0.30 / 1\text{M input tokens}$; $\$0.40 - \$2.50 / 1\text{M output tokens}$ ($\sim 300\text{đ} - 800\text{đ}/\text{buổi}$) |
| **Database & Vector** | Neon PostgreSQL + Auth | Miễn phí **1 GB lưu trữ**, tự ngủ khi vắng khách, miễn phí 60.000 MAU Auth | Tính theo compute thực tế ($\sim \$5 - \$16/\text{tháng}$) |
| **Lưu trữ Cloud (Tùy chọn)** | Cloudflare R2 | Miễn phí **10 GB/tháng**, **$0 phí băng thông tải ra (Zero Egress)** | $\$0.015/\text{GB}/\text{tháng}$ vượt mức |
| **Web Hosting & Thanh toán** | Vercel / Cloudflare Pages + VietQR (SePay) | Hosting $0; nhận chuyển khoản QR cá nhân $0 | Tên miền $\sim 25.000\text{đ}/\text{tháng}$; Webhook tự động VietQR $\sim 70.000\text{đ} - 99.000\text{đ}/\text{tháng}$ khi đông khách |

> **Quy tắc vàng bảo vệ biên lợi nhuận:** Tuyệt đối **không đẩy thẳng tệp âm thanh thô vào LLM đa phương thức** (giá token audio đầu vào khoảng $\$1.00 / 1\text{M tokens}$, đắt gấp $>3$ lần). Đi theo luồng 2 bước (`VAD Client` $\rightarrow$ `Whisper Turbo` $\rightarrow$ `Gemini Flash Text`) giúp tổng giá vốn (COGS) cho 1 buổi họp/phỏng vấn dài 1 tiếng chỉ rơi vào khoảng **$1.300\text{đ} - 2.000\text{đ}$**.

### 4.2. Công thức Điểm hòa vốn & Biên lợi nhuận gói 30 ngày

Với gói **"Vé Săn Việc 30 Ngày"** bán qua mã VietQR giá $P = 99.000\text{đ}$ (bao gồm 10 giờ phân tích phỏng vấn/họp + 15 phiên luyện tập cùng HR ảo):
* Chi phí biến đổi phục vụ 1 khách trả phí ($C_{\text{paid}}$): $\approx 16.500\text{đ}$ tiền API + $500\text{đ}$ phí giao dịch $= 17.000\text{đ}$.
* Lợi nhuận gộp trên mỗi khách trả phí:
  $$\text{Gross Profit} = 99.000\text{đ} - 17.000\text{đ} = 82.000\text{đ} \quad (\text{Biên lợi nhuận gộp } \approx 82,8\%)$$
* Chi phí cho 1 người dùng thử nhận 90–120 phút miễn phí một lần duy nhất ($C_{\text{free}}$): $\approx 2.500\text{đ}$.
* **Tỷ lệ nuôi chéo:** Chỉ cần **1 khách mua gói $99.000\text{đ}$** là đủ bù đắp toàn bộ chi phí API cho **$>30$ người dùng thử miễn phí**. Ở quy mô 100 người đăng ký đầu tiên (giả sử tỷ lệ chuyển đổi $8\%$ tức 8 khách mua), doanh thu đạt $792.000\text{đ}$, tổng chi phí vận hành khoảng $391.000\text{đ}$, dự án **lãi ròng ngay $\sim 401.000\text{đ}$** và hòa vốn chỉ từ khách hàng thứ 3–4.

### 4.3. Năm chiến thuật duy trì vốn 0 đồng trước khi có doanh thu lớn
1. **Client-Side Offloading:** Lọc khoảng lặng VAD và lưu file âm thanh gốc ở `IndexedDB` máy khách để tốn $0 tiền lưu trữ đám mây cho tài khoản miễn phí.
2. **One-Time Trial Credit:** Tặng cố định 90–120 phút dùng thử một lần duy nhất khi tạo tài khoản (đủ cho 2 buổi phỏng vấn thật), **không reset miễn phí hàng tháng** để tránh chảy máu chi phí API định kỳ.
3. **Chế độ BYOK (Bring Your Own Key):** Cho phép dân kỹ thuật tự điền API Key Groq/Gemini cá nhân miễn phí để bạn có tệp người dùng kiểm thử sản phẩm thực tế với chi phí biến đổi bằng $0.
4. **Bán gói cước ngắn hạn không tự gia hạn qua VietQR:** Xóa bỏ tâm lý ngại nhập thẻ Visa/Mastercard; bán gói $79.000\text{đ} - 129.000\text{đ}$ cho 30 ngày cao điểm phỏng vấn và gói chuyên nghiệp $149.000\text{đ} - 199.000\text{đ}/\text{tháng}$ cho người đi làm.
5. **Chào bán sớm 10–15 suất Founding Member:** Thu ngay $199.000\text{đ}/\text{suất}$ (dùng 6 tháng) ngay khi có bản chạy thử tuần thứ 2 để gom $\sim 2.000.000\text{đ} - 3.000.000\text{đ}$ tiền mặt làm vốn lưu động xoay vòng.

---

## 5. LỘ TRÌNH THỰC THI POC 14 NGÀY (4 CỔNG GO / NO-GO)

### Cổng 1 (Ngày 1–3): Kiểm chứng Thu âm Tách kênh & Gỡ băng Anh–Việt
* **Đầu ra tối thiểu:** 1 trang HTML/JS cục bộ dưới 200 dòng code tách 2 kênh (`getDisplayMedia` + `getUserMedia`) lưu vào `IndexedDB` + 1 script Python đo thử `Groq Whisper Large-v3-turbo` và `Soniox` có kèm từ khóa CV/JD.
* **Tiêu chuẩn vượt ải (Go):** Hai kênh không bị lẫn người nói, không vọng âm khi đeo tai nghe, tỷ lệ sai thuật ngữ chuyên ngành Anh–Việt (WER) $< 12\%$, độ lệch timestamp $< 1\text{ giây}$.
* **Việc cấm làm sớm:** Chưa làm trang đăng nhập, chưa làm giao diện cầu kỳ.

### Cổng 2 (Ngày 4–7): Rèn "Khoảnh khắc Wow" với Báo cáo Giải phẫu Hậu kiểm
* **Đầu ra tối thiểu:** Bộ System Prompt trên `Gemini 2.5 Flash` xuất JSON chấm điểm STAR đối chiếu CV/JD, viết lại câu trả lời mẫu nâng cấp và giao diện bấm vào từng nhận xét để phát lại đúng giây âm thanh gốc từ `IndexedDB`.
* **Tiêu chuẩn vượt ải (Go):** Thử nghiệm trên 3 buổi ghi âm thật, từ $80\%$ nhận xét trở lên chỉ trúng điểm ấp úng hoặc thiếu số liệu mà người nói gật đầu công nhận sâu sắc hơn hẳn việc dán chữ vào ChatGPT thường.
* **Việc cấm làm sớm:** Chưa làm đàm thoại giọng nói thời gian thực (Voice-to-Voice).

### Cổng 3 (Ngày 8–10): Dựng Bộ nhớ Lai PostgreSQL & Cổng MCP Cá nhân
* **Đầu ra tối thiểu:** Khởi tạo 3 bảng `sessions`, `qa_pairs`, `weakness_profile` trên Neon Free Tier + 1 Python MCP Server khoảng 100 dòng code cắm vào môi trường làm việc cá nhân.
* **Tiêu chuẩn vượt ải (Go):** Tự đóng vai "Khách hàng số 0" dùng thực tế qua 3–5 buổi họp/luyện phỏng vấn; truy vấn qua MCP tổng hợp đúng lỗi lặp lại trong $< 2\text{ giây}$ và sinh được kịch bản HR hỏi xoáy sát lịch sử.

### Cổng 4 (Ngày 11–14): Kiểm chứng Ví tiền (Concierge MVP) với 10 Người dùng Thật
* **Đầu ra tối thiểu:** Web App tối giản gắn sẵn Google Login của Neon + hiển thị mã VietQR cá nhân kích hoạt gói tay trong 10 giây.
* **Tiêu chuẩn vượt ải (Go):** Mời 10 sinh viên IT sắp ra trường / kỹ sư đang nhảy việc dùng thử miễn phí 1 buổi phỏng vấn thật; có tối thiểu **2–3 người sẵn sàng chuyển khoản tiền thật gói $99.000\text{đ}$**. Khi đạt mốc này mới bắt đầu tích hợp webhook thanh toán tự động và mở rộng giao diện.

---

## 6. QUY TRÌNH VẬN HÀNH PHỐI HỢP GEMINI WEB – NOTEBOOKLM – ANTIGRAVITY IDE

1. **Gemini Web + Gem + Sổ `00_INTERVIEW_MEET_CONTEXT_ENGINE` (Bộ não Nghiên cứu & Kiến trúc):**
   * Xử lý mọi tác vụ khảo sát thị trường, Deep Research, kiểm chứng API mới, thiết kế Schema, tối ưu System Prompt và phản biện mô hình kinh doanh.
2. **Antigravity IDE – Thư mục `Interview-meet` (Động cơ Thực thi Code):**
   * Chuyên trách viết code, chạy thử nghiệm cục bộ, gỡ lỗi trên Terminal và quản lý Git.
3. **Cơ chế đồng bộ 1 chiều sạch ngữ cảnh:**
   * Lưu tệp tài liệu tổng hợp này vào sổ NotebookLM `00_INTERVIEW_MEET_CONTEXT_ENGINE` để Gem luôn giữ trọn bộ nhớ gốc qua mọi phiên chat mới.
   * Đồng thời sao chép nội dung tệp này lưu thành `GEMINI.md` (hoặc `docs/00_MASTER_SPEC.md`) ngay tại thư mục gốc `Interview-meet` trên máy tính và thiết lập quy tắc cốt lõi trong mục **Customizations** của Antigravity để AI bên trình code tuân thủ đúng kiến trúc đã chốt.