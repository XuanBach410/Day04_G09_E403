# Market Data Tool

Tool Python không cần dependency ngoài, cung cấp một phần chức năng tương tự
`yfinance` qua Yahoo Finance public endpoints.

```bash
python3 market_data_tool.py quote --symbol AAPL
python3 market_data_tool.py history --symbol BTC-USD --range 5d --interval 1h
python3 market_data_tool.py search --query "Apple"
python3 whale_market_flow_tool.py HPG
```

Kết quả luôn là JSON. API công khai có thể rate-limit hoặc thay đổi; lỗi được trả
thành JSON rõ ràng. Dữ liệu chỉ nhằm mục đích tham khảo, không phải tư vấn đầu tư.
