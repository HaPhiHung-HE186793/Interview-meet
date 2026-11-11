# NHẬT KÝ Ý TƯỞNG KHỞI NGUỒN, CHIẾN THUẬT VỐN 0 ĐỒNG & SỔ TAY PHỐI HỢP GEMINI WEB – ANTIGRAVITY

> **Nguồn trích xuất:** Tổng hợp từ các Lượt 1–4 và Lượt 6–9 của phiên thảo luận kiến trúc gốc trên Gemini Web (`10–11/11/2026` — https://share.gemini.google/GQgpe9AGNBX2).

---

## 1. Bài Toán Khởi Nguồn Từ Nhu Cầu Thực Tế (Lượt 1)

Ý tưởng gốc xuất phát từ nhu cầu cá nhân xuyên suốt cả lúc **họp dự án** lẫn lúc **đi phỏng vấn online qua Google Meet**:
1. Có một công cụ đóng vai **Thư ký cá nhân tàng hình** ghi nhận toàn bộ nội dung cuộc họp / buổi phỏng vấn mà không đẩy Bot lạ vào phòng gây phản cảm.
2. Lưu trữ có cấu trúc thành **Kho Dữ liệu Ngữ cảnh Cá nhân ("Não thứ hai")** để mỗi khi dùng Gemini, VS Code hay Antigravity hỏi đáp công việc, AI có thể truy cập trực tiếp vào ngữ cảnh riêng của bản thân.
3. Tích lũy toàn bộ các câu hỏi và câu trả lời thực tế qua nhiều đợt phỏng vấn để vận hành **Huấn luyện viên HR Thích ứng**: AI đóng vai HR/Tech Lead lấy đúng những mảng kiến thức hoặc câu hỏi mà người dùng từng trả lời yếu/lấp lửng để hỏi biến tấu, xoáy sâu (`follow-up probe`), chấm điểm đối chiếu quá khứ – hiện tại, chỉ rõ chỗ thiếu, gợi ý cải thiện và yêu cầu trả lời lại cho đến khi hoàn chỉnh.

---

## 2. Năm Chiến Thuật Sống Còn Với Vốn Gần Bằng 0 Đồng (Lượt 3)

Nguyên tắc sống còn khi khởi đầu vốn mỏng: **không để phát sinh chi phí biến đổi định kỳ cho người dùng miễn phí, và rút ngắn tối đa quãng đường tới giao dịch trả tiền đầu tiên.**

1. **Client-Side Offloading (Đẩy việc nặng về trình duyệt người dùng):**
   - Chạy bộ lọc cắt khoảng lặng (`VAD` bằng WebAssembly) ngay trên trình duyệt máy khách để loại bỏ `25%–40%` thời gian phòng họp im lặng trước khi gửi đi gỡ băng.
   - Lưu file ghi âm gốc (`WebM/Opus`) ngay trong `IndexedDB` trên trình duyệt của người dùng; chỉ đẩy bản JSON tóm tắt và hồ sơ điểm yếu (vài chục KB văn bản) lên Neon PostgreSQL (`1 GB` miễn phí chứa được hàng nghìn người dùng).
2. **One-Time Trial Credit (Hạn mức dùng thử một lần duy nhất):**
   - Tuyệt đối không tặng phút miễn phí tự làm mới hàng tháng (tránh chảy máu tiền API định kỳ).
   - Tặng cố định `90–120 phút` trải nghiệm duy nhất cho mỗi tài khoản mới — vừa đủ cho 2 buổi phỏng vấn thật để người dùng trải nghiệm "khoảnh khắc giật mình" khi thấy AI chỉ đúng giây ấp úng, và buộc nâng cấp ở buổi thứ 3 hoặc khi mở phòng luyện HR Ảo.
3. **Chế độ BYOK (`Bring Your Own Key`):**
   - Cho phép lập trình viên/người dùng kỹ thuật tự gắn API Key cá nhân (Google AI Studio / Groq đều có hạn mức miễn phí hằng ngày) để có tệp kiểm thử thực chiến với chi phí vận hành bằng `0 đồng`.
4. **Bán "Vé Chiến Dịch Săn Việc 30 Ngày" qua VietQR:**
   - Giải quyết tâm lý ngại nhập thẻ quốc tế và sợ trừ tiền tự động hàng tháng của ứng viên Việt Nam.
   - Gói `99.000đ / 30 ngày` (10 giờ phân tích họp/phỏng vấn + 15 phiên luyện HR ảo) chỉ tốn `~16.500đ–17.000đ` giá vốn API + giao dịch, mang lại biên lợi nhuận gộp `~82.000đ` (`~82,8%`). Chỉ cần **1 khách trả tiền là nuôi đủ chi phí thử nghiệm cho `>30` người dùng miễn phí**, hòa vốn ngay từ khách hàng thứ 3–4.
5. **Chào bán sớm 10–15 suất `Founding Member`:**
   - Ngay cuối Tuần 2 khi luồng thu âm tách kênh + Báo cáo Giải phẫu Hậu kiểm chạy chuẩn, mở 10–15 suất `Founding Member` giá `199.000đ` (dùng 6 tháng) để thu ngay `~2.000.000đ – 3.000.000đ` tiền mặt làm vốn lưu động xoay vòng.

---

## 3. Nguyên Tắc "3 Không" Trong 14 Ngày PoC Đầu Tiên (Lượt 6)

1. **Không làm hệ thống phụ trợ sớm:** Bỏ qua trang giới thiệu bóng bẩy, luồng quên mật khẩu phức tạp hay xuất hóa đơn tự động ở những ngày đầu; khi tới Cổng 4 chỉ dùng Google Login dựng sẵn của Neon/Supabase (tốn 15 phút) và kích hoạt gói VietQR thủ công (tốn 10 giây).
2. **Không đóng gói Desktop App hay chờ duyệt Chrome Web Store:** Chạy trực tiếp trên nền tảng Web chuẩn để sửa lỗi trong 5 phút là người dùng thử nghiệm nhận được ngay.
3. **Không mở rộng đa ngành vội:** Tập trung 100% cho dân IT & kỹ thuật song ngữ Anh–Việt gật đầu khen *"Bắt thuật ngữ chuẩn thật, chấm đúng chỗ mình bí!"* trước tiên.

---

## 4. Quy Trình "1 Não Nghiên Cứu – 1 Tay Thực Thi" & Bản Sao Cấu Hình Gem (Lượt 7–9)

### 4.1. Phân vai rõ ràng giữa hai môi trường
- **Gemini Web + Sổ NotebookLM `00_INTERVIEW_MEET_CONTEXT_ENGINE` + Gem `Interview-Meet Partner & Architect`:** Đóng vai trò **Bộ não Hướng ngoại & Chiến lược** (Deep Research hàng trăm nguồn web, khảo sát giá đối thủ, thiết kế Rubric chấm điểm, phản biện mô hình kinh doanh).
- **Antigravity IDE (Thư mục `Interview-meet`):** Đóng vai trò **Bộ não Hướng nội & Thực thi** (viết code, kiểm thử Web Audio / Python / PostgreSQL / MCP trên Terminal và quản lý Git), tự động đọc ngữ cảnh sạch từ [GEMINI.md](../GEMINI.md) và quy tắc [.agents/rules/interview-meet-architect.md](../.agents/rules/interview-meet-architect.md).

### 4.2. Bản lưu System Instructions của Gem `Interview-Meet Partner & Architect` (dùng trên Gemini Web)
Lưu trữ nguyên văn bên dưới để tái sử dụng hoặc cập nhật trên giao diện Gemini Web (gắn kèm nguồn Knowledge là sổ NotebookLM `00_INTERVIEW_MEET_CONTEXT_ENGINE`):

```markdown
# VAI TRÒ CỐT LÕI
Bạn là Co-founder Kỹ thuật & Chiến lược Sản phẩm (Thinking Partner) của dự án **Interview-Meet Context Engine** — nền tảng Thư ký Họp không dùng bot, Bộ nhớ Ngữ cảnh Cá nhân chuẩn MCP và Huấn luyện viên Phỏng vấn Thích ứng (Post-Call Debrief + Adaptive HR Coach) tập trung vào ngách kỹ sư phần mềm, nhân sự IT và người làm việc chuyên môn song ngữ Anh–Việt.

# NGUỒN TRI THỨC BẮT BUỘC TRA CỨU
Trước khi trả lời bất kỳ câu hỏi nào về thiết kế tính năng, database, lựa chọn API, định giá, đối thủ hay lộ trình làm việc, bạn PHẢI tra cứu sổ ghi chú `00_INTERVIEW_MEET_CONTEXT_ENGINE` đã được gắn trong phần Kiến thức để giữ tính nhất quán tuyệt đối với các quyết định đã chốt.

# KỶ LUẬT KIẾN TRÚC & CHIẾN LƯỢC KHÔNG ĐƯỢC ĐI LỆCH
1. **Thu âm tách 2 kênh không dùng Bot:** Luôn ưu tiên kiến trúc Web Audio API (`getDisplayMedia` cho tab Meet + `getUserMedia` cho Micro) lưu đối chiếu âm thanh nén cục bộ (`IndexedDB` / ổ cứng mã hóa) gắn mốc giây để kiểm chứng số liệu. Tuyệt đối không đề xuất làm Bot chui vào phòng họp hay gửi email spam.
2. **Định vị minh bạch, nói không với Stealth Cheating:** Tập trung vào luyện phản xạ trước giờ G và Báo cáo Giải phẫu Hậu kiểm (Post-Call Debrief) + vòng lặp HR ảo hỏi xoáy vào lỗ hổng cũ. Không thiết kế công cụ nhắc bài gian lận trực tiếp.
3. **Tối ưu chi phí vốn 0 đồng (Unit Economics):** Luôn tách quy trình 2 bước (lọc khoảng lặng VAD tại client -> STT giá rẻ hỗ trợ code-switching Anh–Việt như Groq Whisper Turbo / Soniox kèm từ điển CV/JD -> LLM nhẹ như Gemini 2.5 Flash phân tích văn bản). Giữ cơ sở dữ liệu lai 3 tầng trên PostgreSQL + `pgvector` (`sessions`, `qa_pairs`, `weakness_profile`).
4. **Cầu nối đồng bộ sang Antigravity IDE:** Tôi dùng bạn trên Gemini Web làm "Bộ não Nghiên cứu & Kiến trúc", còn việc viết code thực thi diễn ra tại dự án `Interview-meet` trên Antigravity IDE. Mỗi khi chúng ta chốt thay đổi kiến trúc hoặc hoàn thành thiết kế một module mới, hãy chủ động đề xuất xuất bản cập nhật ngắn gọn chuẩn Markdown để tôi dán sang file `GEMINI.md` hoặc thư mục `docs/` bên Antigravity, đồng thời nhắc tôi nếu cần lưu bổ sung vào NotebookLM.

# PHONG CÁCH PHỐI HỢP
- Đi thẳng vào giải pháp thực chiến, có số liệu chi phí và đánh giá rủi ro rõ ràng.
- Sẵn sàng phản biện thẳng thắn nếu một ý tưởng mới làm phình chi phí API, dễ bị đối thủ clone trong 48 giờ hoặc đi chệch khỏi lộ trình kiểm chứng 4 cổng Go/No-Go.
```
