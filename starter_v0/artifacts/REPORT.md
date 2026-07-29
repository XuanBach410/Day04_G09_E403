# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 11:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- Team: G09_E403
- Members: 
- Provider/model: OpenAI (gpt-4o-mini)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Trợ lý AI chuyên nghiên cứu thị trường chứng khoán: Tra cứu dữ liệu thị trường (như yfinance: giá gần nhất, lịch sử OHLCV), cập nhật tin tức tài chính, tìm kiếm diễn biến dư luận trên mạng xã hội về các mã chứng khoán và tổng hợp thành bản tin ngắn gọn.

**Link dùng thử (truy cập được trong showdown):**

> URL: Localhost:8501

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | lấy bài đăng gần đây của một tài khoản Twitter | không |
| social_search | tìm bài đăng theo từ khóa trên mạng xã hội | không |
| lookup | tra cứu tin tức, thông tin thị trường trên internet | không |
| fetch | đọc và trích xuất nội dung từ một địa chỉ URL | không |
| market_data | tra cứu dữ liệu thị trường chứng khoán (giá, lịch sử OHLCV, tìm mã) | CÓ (Tool nhóm tự làm) |

## A3. Câu hỏi mẫu để thử

1. Lấy dữ liệu giá 5 phiên gần nhất của mã cổ phiếu FPT giúp mình.
2. Tin tức thị trường chứng khoán hôm nay có gì nổi bật?
3. Mọi người trên Twitter đang bàn tán gì về cổ phiếu VNM?
4. Đọc giúp tôi bài viết này và tóm tắt những ý chính: [dán một URL bài báo tài chính]
5. Tìm tin tức về Vingroup và giá cổ phiếu VIC hôm nay.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
|---|---|---|---|
| 1. Hỏi giá CP nhưng quên ghi mã | `clarify` được gọi để hỏi mã CP | v0 tự đoán bừa mã $\rightarrow$ v1 biết gọi `clarify` hỏi lại | transcripts/demo1.json |
| 2. Hỏi tin tức chứng khoán | `lookup` với `query` tinh gọn | v0 nhét từ "tin tức" vào query $\rightarrow$ v2 tách từ khóa lõi | transcripts/demo2.json |
| 3. Song song lấy tin và giá cổ phiếu | `lookup` & `market_data` chạy song song | Minh họa agent xử lý yêu cầu phức tạp từ người dùng | transcripts/demo3.json |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Prompt/tool change | Hypothesis | Metric name | Before | After | Run File |
|---|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |  |
| v1 |  |  |  |  |  |  |
| v2 |  |  |  |  |  |  |
| v3 |  |  |  |  |  |  |

## B2. Failure analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

## B3. Team eval cases

List the 10 cases added to `data/eval_group.json`:

- 5 single-turn
- 5 multi-turn

This section is for the mandatory team-authored eval set. Optional built-ins do
not belong here.

File template để trống có chủ đích; nhóm phải tự thiết kế đủ 10 case.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live chat evidence

Use `transcripts/*.transcript.json`.

| Scenario/Turn | Version | Tool Calls + Args | Transcript/Run | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Tool capability evidence

Phân loại rõ tool mới bắt buộc, optional built-in và tool đủ điều kiện bonus. Chỉ ghi Telegram/PDF nếu nhóm thực sự dùng; base report không cần chúng.

UI is core deliverable, not bonus. Do not list it here.

| Category | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Must-have: tool mới đầu tiên |  |  |  |
| Optional built-in |  |  |  |
| Bonus: tool mới thứ 4 trở đi |  |  |  |

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?
