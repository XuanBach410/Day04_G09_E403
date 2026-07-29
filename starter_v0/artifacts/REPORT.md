# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. Xong trước 11:30 để làm tài liệu phụ trợ khi demo.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. Có thể hoàn thiện sau buổi debate để nộp bài.

## Team

- Team: G09_E403
- Members:
  1. **Trần Xuân Bách** (Nhóm trưởng - 2003 - 2A202601093)
  2. **Nguyễn Duy Trọng** (Thành viên - 2001 - 2A202601333)
  3. **Đinh Hoài Nam** (Thành viên - 2005 - 2A202601889)
  4. **Nguyễn Hoàng Tín** (Thành viên - 2005 - 2A202601603)
  5. **Trịnh Quốc Trọng** (Thành viên - 2003 - 2A202601779)
  6. **Hà Ngọc Minh** (Thành viên - 2005 - 2A202602028)
  7. **Bùi Thế Huy** (Thành viên - 2004 - 2A202601881)
  8. **Phạm Thị Thuỳ Linh** (Thành viên - 2004 - 2A202601181)
- Provider/model: OpenAI (gpt-4o-mini) / OpenRouter

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent chuyên sâu ngành Tài chính & Thị trường Chứng khoán Việt Nam: Tra cứu dữ liệu giao dịch cổ phiếu thực tế, cập nhật tin tức vĩ mô, quét dư luận trên mạng xã hội, đọc trích xuất bài báo khoa học (arXiv) và tự động đóng gói báo cáo digest chuyên nghiệp.

**Link dùng thử (truy cập được trong showdown):**

> Localhost UI: `http://localhost:8501`  
> Public Tunnel URL: `https://socks-surround-garlic-issued.trycloudflare.com`

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `get_stock_info` | Tra cứu dữ liệu tài chính & giá lịch sử chứng khoán VN | CÓ (Tool mới của nhóm) |
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc cần xác nhận | Không |
| `timeline` | Lấy danh sách bài đăng mới nhất từ một tài khoản xã hội | Không |
| `social_search` | Tìm kiếm bài đăng theo từ khóa trên mạng xã hội | Không |
| `lookup` | Tra cứu tin tức và thông tin tổng quát trên Internet | Không |
| `fetch` | Đọc và trích xuất nội dung chi tiết từ một URL | Không |
| `format` | Đóng gói dữ liệu thành bản tin digest/markdown chuẩn | Không |
| `send` | Gửi văn bản/thông báo (có cờ xác nhận) | Không |
| `policy` | Tra cứu tài liệu quy định nội bộ công ty | Không |
| `papers` | Tìm kiếm bài báo khoa học trên arXiv | Không |
| `paper_text` | Đọc trích xuất nội dung text từ file PDF bài báo arXiv | Không |

## A3. Câu hỏi mẫu để thử

1. Lấy thông tin tài chính và giá giao dịch mới nhất của mã cổ phiếu HPG.
2. Tra cứu 3 tin tức mới nhất về ngành AI/Công nghệ tại Việt Nam tuần qua và tóm tắt dạng brief.
3. Tìm 3 bài báo khoa học gần đây nhất trên arXiv về LLM Agent trong tài chính.
4. Tra cứu quy định bảo mật data privacy của công ty, sau đó gửi tóm tắt qua Telegram.

## A4. Kịch bản demo đã rehearse

| Scenario | Tool trace cần thấy | Câu chuyện cải thiện version | Fallback run/transcript |
|---|---|---|---|
| 1. Tra cứu cổ phiếu thiếu mã | `clarify(response_type="text")` | v0 đoán bừa mã $\rightarrow$ v1 hỏi lại làm rõ thông tin | `transcripts/v1_openai_demo1.transcript.json` |
| 2. Gửi báo cáo cần xác nhận | `clarify` $\rightarrow$ `send(confirmed=True)` | v0 tự gửi tin nhắn $\rightarrow$ v2 có cờ xác nhận an toàn | `transcripts/v2_openai_demo2.transcript.json` |
| 3. Nghiên cứu đa bước (Search + Fetch + Format) | `lookup` $\rightarrow$ `fetch` $\rightarrow$ `format` | v1 gọi tool rời rạc $\rightarrow$ v3 chạy chuỗi 3 vòng hoàn chỉnh | `transcripts/v3_openrouter_demo3.transcript.json` |

---

# PHẦN B — Chi tiết / Bằng chứng

> Điều kiện metric hợp lệ: `provider_error_cases` phải bằng `0`; `measured_cases` phải bằng `total_cases`; và bất kỳ `tool_results` nào có error đều phải được review thủ công vì routing PASS không chứng minh tool execution đã đúng.

## B1. Version evidence

Dữ liệu trích xuất trực tiếp từ các file chạy trong thư mục `runs/`.

| Version | Prompt/tool change | Hypothesis | Metric name | Before | After | Run File |
|---|---|---|---|---:|---:|---|
| v0 | Baseline initial system prompt & tools | Baseline routing accuracy | Tool Routing Accuracy | 0.0% | 100.0% | `runs/v0_B_base_openai_20260729T104815264395.json` |
| v1 | Thêm hướng dẫn clarify & quy tắc tham số query | Giảm tỷ lệ chọn sai tool khi thiếu thông tin | Case Accuracy | 85.0% | 95.0% | `runs/v1_B_base_openai_20260729T105037205832.json` |
| v2 | Bổ sung confirmation boundary cho tool `send` | Đảm bảo phải có xác nhận yes/no trước khi gọi send | Multiturn Accuracy | 90.0% | 100.0% | `runs/v2_B_base_openai_20260729T105425768465.json` |
| v3 | Đăng ký tool mới `get_stock_info` & đồng bộ schema | Đạt độ chính xác tuyệt đối trên cả base eval & openrouter | Case Accuracy | 95.0% | 100.0% | `runs/v3_B_base_openrouter_20260729T104846682720.json` |

## B2. Failure analysis

Chi tiết phân tích lỗi thực tế ghi nhận từ các lượt chạy thử nghiệm:

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R01_user_tweets_routing` | `wrong_tool` | `lookup(query="Sam Altman tweet")` | Model gọi tra cứu web thay vì đọc timeline tài khoản | Sửa `artifacts/tools.yaml` mô tả rõ `timeline` dùng cho bài đăng của 1 cá nhân cụ thể. |
| `R06_timeframe_arg` | `wrong_arg_value` | `lookup(timeframe="month")` | Model truyền tham số timeframe='month' cho yêu cầu "tuần này" | Thêm quy định rõ trong `system_prompt.md`: "tuần này" $\rightarrow$ `timeframe="week"`. |
| `R10_send_confirmation` | `wrong_boundary` | `send(confirmed=False)` | Model tự động gọi `send` khi người dùng chưa bấm xác nhận | Thêm luồng `clarify(response_type="yes_no")` yêu cầu xác nhận trước khi thực hiện. |

## B3. Team eval cases

Danh sách 10 case test do nhóm tự thiết kế trong `data/eval_group.json`:

- 5 Single-turn
- 5 Multi-turn

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_stock_info_routing` | Tra cứu thông tin cổ phiếu chứng khoán Việt Nam | `get_stock_info(symbol="HPG")` | PASS |
| `G02_papers_search_routing` | Tìm kiếm bài báo khoa học trên arXiv | `papers(query="LLM Agent", max_results=5)` | PASS |
| `G03_paper_text_extraction` | Đọc trích xuất text từ file PDF bài báo arXiv | `paper_text(arxiv_url="2312.00001")` | PASS |
| `G04_policy_lookup` | Tra cứu tài liệu quy định nội bộ công ty | `policy(query="data privacy", policy_area="data_privacy")` | PASS |
| `G05_out_of_scope_general_chat` | Xử lý câu chào hỏi xã giao ngoài phạm vi | `no_tool=true` | PASS |
| `G06_multiturn_clarify_stock` | Hỏi làm rõ khi thiếu mã CP $\rightarrow$ gọi tool | Turn 1: `clarify` $\rightarrow$ Turn 2: `get_stock_info` | PASS |
| `G07_multiturn_send_confirmation` | Yêu cầu cờ xác nhận trước khi gửi tin nhắn | Turn 1: `clarify(yes_no)` $\rightarrow$ Turn 2: `send(confirmed=True)` | PASS |
| `G08_multiturn_search_and_format` | Tìm kiếm tin tức rồi định dạng báo cáo | Turn 1: `lookup` $\rightarrow$ Turn 2: `format(template="brief")` | PASS |
| `G09_multiturn_social_and_user_timeline` | Quét mạng xã hội $\rightarrow$ xem timeline cá nhân | Turn 1: `social_search` $\rightarrow$ Turn 2: `timeline` | PASS |
| `G10_multiturn_web_search_and_fetch` | Tra cứu tổng quan $\rightarrow$ đọc nội dung chi tiết URL | Turn 1: `lookup` $\rightarrow$ Turn 2: `fetch` | PASS |

## B4. Live chat evidence

Bằng chứng từ các lượt chạy thực tế lưu trong `transcripts/*.transcript.json`:

| Scenario/Turn | Version | Tool Calls + Args | Transcript/Run | Outcome |
|---|---|---|---|---|
| Tra cứu giá HPG | v3 | `get_stock_info(symbol="HPG")` | `transcripts/v3_openrouter_stock.json` | Trả về giá hiện tại, biến động % và vốn hóa chính xác. |
| Tìm bài báo arXiv | v3 | `papers(query="LLM Agent")` | `transcripts/v3_openrouter_arxiv.json` | Trích xuất 5 bài báo khoa học mới nhất từ arXiv kèm link. |
| Hỏi đáp quy định | v2 | `policy(query="data privacy")` | `transcripts/v2_openai_policy.json` | Đọc đúng nội dung policy và tóm tắt theo các điều khoản. |

## B5. Tool capability evidence

| Category | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Must-have: tool mới đầu tiên | `tools/get_stock_info/` | Đã tích hợp API tra cứu chứng khoán VN thành công | Giới hạn xử lý khi người dùng nhập sai tên mã cổ phiếu. |
| Optional built-in | `tools/papers/`, `tools/policy/` | Đã đăng ký và chạy mượt trên cả eval & live chat | Giới hạn số trang đọc PDF để tránh vượt context window. |

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**: Các quy tắc ưu tiên chọn tool (routing priority), quy định ánh xạ từ từ ngữ tự nhiên sang enum tham số (ví dụ "tuần này" $\rightarrow$ `timeframe="week"`).
- **Which fixes belonged in `tools.yaml`**: Viết lại mô tả `description` chi tiết cho từng tool, làm rõ phạm vi sử dụng (khi nào dùng `timeline` vs `social_search`) và nêu rõ default values.
- **Which failure needed manual review instead of automatic grading?**: Các trường hợp tool gọi đúng nhưng API bên thứ 3 trả về lỗi (VD: RapidAPI 429 Too Many Requests) hoặc khi model đưa ra câu trả lời giải thích tự nhiên mà grader tự động không bắt hết được context.
- **What would you improve next?**: Tích hợp thêm biểu đồ nến (Candlestick Chart) cho giá cổ phiếu ngay trên Streamlit Web UI và bổ sung bộ nhớ lưu trữ dài hạn (Long-term Memory) cho Agent.
