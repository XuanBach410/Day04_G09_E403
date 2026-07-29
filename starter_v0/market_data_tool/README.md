# Market Data Tool

Tool Python không cần thư viện ngoài (chỉ sử dụng thư viện chuẩn của Python), cung cấp các chức năng tra cứu dữ liệu thị trường công khai từ Yahoo Finance (tương tự một phần `yfinance`).

---

## 1. Tính năng chính (Actions)

Tool hỗ trợ 3 thao tác chính (`action`):

1. **`quote`**: Tra cứu giá gần nhất/mới nhất của một mã tài sản (cổ phiếu, crypto, chỉ số...).
   - Trả về: `symbol`, `short_name`, `price`, `previous_close`, `currency`, `exchange`, `market_state`, `as_of`.
   - Tham số bắt buộc: `symbol`.

2. **`history`**: Tra cứu lịch sử chuỗi giá OHLCV (Open, High, Low, Close, Volume).
   - Trả về: danh sách các hàng dữ liệu mốc thời gian kèm thông số OHLCV.
   - Tham số bắt buộc: `symbol`.
   - Tham số tùy chọn:
     - `range`: Khoảng thời gian lịch sử (`1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`). Mặc định: `1mo`.
     - `interval`: Tần suất dữ liệu (`1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `3mo`). Mặc định: `1d`.

3. **`search`**: Tìm kiếm mã chứng khoán/tài sản theo từ khóa tên hoặc mã.
   - Trả về: danh sách các mã tìm thấy kèm tên, loại tài sản và sàn giao dịch.
   - Tham số bắt buộc: `query`.
   - Tham số tùy chọn:
     - `limit`: Số lượng kết quả tối đa (từ 1 đến 20, mặc định: 8).

---

## 2. Hướng dẫn sử dụng CLI

Chạy trực tiếp file Python từ dòng lệnh:

```bash
# 1. Lấy thông tin giá mới nhất
python3 market_data_tool.py quote --symbol AAPL

# 2. Lấy dữ liệu lịch sử giá
python3 market_data_tool.py history --symbol BTC-USD --range 5d --interval 1h

# 3. Tìm kiếm mã theo từ khóa
python3 market_data_tool.py search --query "Apple" --limit 5
```

---

## 3. Hướng dẫn sử dụng trong Python

```python
from market_data_tool import market_data

# Lấy giá mới nhất
quote_info = market_data(action="quote", symbol="AAPL")

# Lấy lịch sử giá 1 tháng
history_info = market_data(action="history", symbol="BTC-USD", range_="1mo", interval="1d")

# Tìm kiếm mã
search_info = market_data(action="search", query="Apple", limit=5)
```

---

## 4. Khai báo Schema cho Agent (`tool.yaml`)

File `tool.yaml` đi kèm định nghĩa schema cho LLM Agent tương thích với định dạng Function Calling / Tool Calling:

- **`clarify`**: Tool hỗ trợ Agent gửi câu hỏi làm rõ nhu cầu với người dùng.
- **`market_data`**: Tool tra cứu dữ liệu thị trường với các enum action (`quote`, `history`, `search`) và các thuộc tính tương ứng.

---

## 5. Lưu ý & Xử lý lỗi

- **Định dạng kết quả**: Luôn trả về dữ liệu định dạng **JSON**.
- **Xử lý lỗi**: Lỗi kết nối hoặc thông tin không hợp lệ được bắt qua `MarketDataError` và xuất thành JSON với key `"error"`.
- **Giới hạn API**: Yahoo Finance public API có thể bị rate-limit hoặc thay đổi cấu trúc endpoint.
- **Khuyến cáo**: Dữ liệu chỉ nhằm mục đích tham khảo, không sử dụng cho mục đích tư vấn đầu tư tài chính chính thức.

