# 🤖 Financial & Market Research Agent — Day 04 Lab v2 (Team G09_E403)

Dự án xây dựng **Research Agent tự động hóa phân tích tài chính & thị trường chứng khoán** chạy bằng AI Provider thật (OpenAI / OpenRouter), tích hợp hệ thống tool tra cứu đa dạng, đánh giá routing evidence-driven và giao diện Web UI "Đấu trường AI" hỗ trợ so sánh song song 4 phiên bản Agent.

---

## 👥 Thông tin Nhóm (Team G09_E403)

- **Trưởng nhóm**: Trần Xuân Bách (2A202601093)
- **Thành viên**:
  1. Nguyễn Duy Trọng (2A202601333)
  2. Đinh Hoài Nam (2A202601889)
  3. Nguyễn Hoàng Tín (2A202601603)
  4. Trịnh Quốc Trọng (2A202601779)
  5. Hà Ngọc Minh (2A202602028)
  6. Bùi Thế Huy (2A202601881)
  7. Phạm Thị Thuỳ Linh (2A202601181)

---

## 🌟 Chức năng cốt lõi của Agent

Agent có khả năng tự động xử lý các tác vụ phức tạp trong lĩnh vực tài chính & nghiên cứu:

1. **Phân tích Chứng khoán Việt Nam**: Tra cứu giá lịch sử, tổng quan doanh nghiệp và các chỉ số tài chính (`vnstock_tool` / `get_stock_info`).
2. **Phát hiện Dòng tiền Cá Voi & Thanh khoản**: Phân tích đột biến khối lượng giao dịch so với SMA20, phát hiện tín hiệu cá voi mua gom hoặc xả hàng (`market_flow`).
3. **Tra cứu Thị trường Quốc tế & Crypto**: Đọc dữ liệu giá công khai Yahoo Finance không phụ thuộc thư viện ngoài (`market_data` - `quote`, `history`, `search`).
4. **Thu thập Tin tức & Tổng hợp Báo cáo**: Tìm kiếm tin tức web (`lookup`), trích nội dung trang (`fetch`), và đóng gói báo cáo dạng digest markdown (`format`).
5. **Nghiên cứu Bài báo Khoa học**: Tìm kiếm và đọc toàn văn PDF các bài báo arXiv (`papers`, `paper_text`).
6. **Làm rõ nhu cầu & Kiểm soát hành động**: Hỏi lại khi thông tin chưa rõ hoặc khi cần xác nhận trước hành động nhạy cảm (`clarify`, `send`).

---

## 🛠️ Danh sách Tool hệ thống (Tool Tracks)

### 🚀 Tool tự phát triển của Nhóm (Team Custom Tools)
- **`market_data`** (`new_tool/market_data_tool.py`): Tra cứu dữ liệu thị trường công khai từ Yahoo Finance (tương tự `yfinance`). Hỗ trợ lấy giá gần nhất (`quote`), lịch sử OHLCV (`history`), và tìm kiếm mã (`search`). Không cần dependency ngoài.
- **`market_flow`** (`starter_v0/tools/market_flow/`): Phân tích dòng tiền cá voi & thanh khoản thị trường. Cảnh báo các sự kiện Cá Voi mua gom/xả hàng (`whale_alerts_count`, `whale_detected_events`).
- **`vnstock_tool`** (`starter_v0/tools/vnstock_tool/`): Tra cứu dữ liệu tài chính & giá chứng khoán Việt Nam qua `vnstock` (`get_stock_info`, `get_company_overview`, `get_financial_ratio`, `get_stock_price`).

### 📦 Tool mặc định & Nâng cao (Core & Extension Tools)
- **`clarify`**: Hỏi lại người dùng khi thiếu tham số hoặc cần xác nhận trước hành động.
- **`lookup`**: Tìm kiếm thông tin & tin tức trực tuyến trên Internet.
- **`fetch`**: Trích xuất nội dung văn bản từ một URL cụ thể.
- **`format`**: Định dạng danh sách thông tin thu thập được thành bản tin markdown digest.
- **`timeline`**: Lấy danh sách bài đăng gần nhất của một tài khoản mạng xã hội.
- **`social_search`**: Tìm kiếm bài đăng theo từ khóa trên mạng xã hội.
- **`policy`**: Tra cứu các quy định & chính sách nội bộ công ty.
- **`papers`**: Tìm kiếm bài báo nghiên cứu khoa học trên arXiv.
- **`paper_text`**: Đọc và trích xuất văn bản từ file PDF bài báo arXiv.
- **`send`**: Gửi thông báo/văn bản (có cờ xác nhận yes/no).

---

## 🖥️ Giao diện Web UI — "Đấu Trường AI"

Hệ thống cung cấp ứng dụng Web UI xây dựng bằng Streamlit cho phép người dùng nhập 1 câu hỏi duy nhất và **so sánh song song kết quả xử lý của 4 phiên bản Agent**:

- **V3 (Phép thuật - Auto Fallback)**: Cấu hình prompt cao nhất, tự động xử lý và chuyển hướng tool fallback thông minh.
- **V2 (Thiên tài - 100đ)**: Tối ưu hoàn hảo tool routing & argument extraction.
- **V1 (Thông minh - 85đ)**: Phiên bản nâng cấp từ baseline.
- **V0 (Ngốc nghếch - Gốc)**: Phiên bản baseline ban đầu.

---

## 🚀 Hướng dẫn Cài đặt & Khởi chạy

### 1. Chuẩn bị môi trường

```bash
cd starter_v0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Cấu hình API Key

Tạo file `.env` từ template và điền API Key (OpenAI / OpenRouter / VNAI):

```bash
cp .env.example .env
```

Kiểm tra kết nối provider:

```bash
python scripts/preflight_provider.py --provider openrouter
```

### 3. Chạy ứng dụng Web UI (Streamlit)

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`.

### 4. Chạy Eval & Benchmark

Chạy bộ đánh giá cố định (Base Suite) cho phiên bản Agent `v3`:

```bash
python run_eval.py --provider openrouter --version v3 --suite base --eval-cases data/eval_base.json
```

Chạy bộ đánh giá 10 test case do nhóm tự viết (Group Suite):

```bash
python run_eval.py --provider openrouter --version v3 --suite group --eval-cases data/eval_group.json
```

---

## 📁 Cấu trúc Dự án

```text
├── README.md                           # Tài liệu giới thiệu tổng quan dự án nhóm
├── TOOL-SETUP.md                       # Hướng dẫn chi tiết setup & API Key
├── new_tool/                           # Tool mới market_data (Python chuẩn, zero external dependency)
│   ├── market_data_tool.py             # Implementation quote / history / search
│   ├── tool.yaml                       # Khai báo schema cho Agent
│   └── README.md                       # Tài liệu hướng dẫn sử dụng market_data
└── starter_v0/                         # Mã nguồn ứng dụng chính & Agent core
    ├── app.py                          # Streamlit Web UI (Đấu Trường AI so sánh 4 phiên bản)
    ├── chat.py                         # Agent loop & xử lý multi-turn conversation
    ├── run_eval.py                     # Script tự động chạy benchmark eval suite
    ├── artifacts/                      # System prompts, tools.yaml, REPORT.md, version_log.csv
    │   ├── system_prompt_v0.md ~ v3.md # Các phiên bản system prompt của nhóm
    │   ├── tools.yaml                  # Khai báo tất cả tools khả dụng
    │   └── REPORT.md                   # Báo cáo đánh giá chi tiết
    ├── data/                           # Các bộ dữ liệu đánh giá (eval_base.json, eval_group.json)
    ├── tools/                          # Thư mục chứa triển khai của từng tool
    │   ├── market_flow/                # Tool phân tích dòng tiền cá voi
    │   ├── vnstock_tool/               # Tool dữ liệu chứng khoán Việt Nam
    │   └── ...
    └── scripts/                        # Scripts kiểm tra preflight & parse kết quả run
```

---

## 📊 Bằng chứng & Đánh giá (Evidence-Driven Evaluation)

Mọi cải tiến từ `V0` đến `V3` đều dựa trên dữ liệu thực nghiệm lưu trong `starter_v0/runs/` và `starter_v0/artifacts/version_log.csv`. 

Thông tin chi tiết về quá trình tối ưu prompt, failure analysis và kết quả benchmark được trình bày đầy đủ tại [starter_v0/artifacts/REPORT.md](starter_v0/artifacts/REPORT.md).
