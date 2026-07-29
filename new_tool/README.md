# Thư mục Tools mở rộng (New Tools)

Thư mục này chứa các tool Python mở rộng phân tích dữ liệu tài chính & thị trường chứng khoán cho Research Agent.

---

## 1. Market Data Tool (`market_data_tool.py`)

Tool Python cung cấp chức năng tra cứu dữ liệu chứng khoán / crypto qua Yahoo Finance public endpoints:

```bash
python3 market_data_tool.py quote --symbol AAPL
python3 market_data_tool.py history --symbol BTC-USD --range 5d --interval 1h
python3 market_data_tool.py search --query "Apple"
```

---

## 2. Whale Market Flow Tool (`whale_market_flow_tool.py`)

Tool phân tích dòng tiền Cá Voi (Whale Flow) và nhận diện trạng thái thanh khoản thị trường (ảm đạm vs sôi động trở lại) dựa trên khối lượng bùng nổ so với đường trung bình động 20 phiên (SMA20).

### Cách sử dụng CLI:
```bash
python3 whale_market_flow_tool.py HPG
```

### Các tính năng chính:
- **Cá Voi mua/bán gom**: Phát hiện các phiên có khối lượng vượt ngưỡng `threshold_multiplier` (mặc định 2.0x SMA20) kết hợp với biến động giá.
- **Trạng thái thanh khoản**: Phân loại thị trường thành `ẢM ĐẠM / MUA BÁN ÍT` (Volume < 0.6x SMA20) hoặc `SÔI ĐỘNG TRỞ LẠI` (Volume >= 1.5x SMA20).
- **Hỗ trợ Fallback kép**: Tự động dùng `vnstock` nếu có, hoặc tự động fallback qua Yahoo Finance API nếu thiếu dependency.

---

## 3. Đăng ký Tool trong Agent (`tool.yaml`)

Cả 2 tool trên đã được khai báo schema đầy đủ trong [tool.yaml](file:///d:/Studying/Code%20VinUni/Lab%204%202907/Day04_G09_E403/new_tool/tool.yaml):
- `market_data`: Tra cứu giá, lịch sử OHLCV, tìm kiếm mã.
- `whale_market_flow`: Phân tích dòng tiền cá voi & trạng thái thanh khoản.

Kết quả trả về luôn là chuẩn định dạng JSON cho LLM dễ dàng xử lý.
