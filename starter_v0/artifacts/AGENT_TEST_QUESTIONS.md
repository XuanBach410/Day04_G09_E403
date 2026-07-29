# Agent Test Questions

Các câu hỏi dưới đây được viết rõ intent, đủ tham số, và có expected tool để agent dễ pass khi demo/eval thủ công.

| # | Câu hỏi test | Expected tool | Expected args chính |
|---|---|---|---|
| 1 | Giá gần nhất của AAPL là bao nhiêu? | `market_data` | `action="quote"`, `symbol="AAPL"` |
| 2 | Lấy lịch sử giá NVDA trong 1 tháng, interval 1 ngày. | `market_data` | `action="history"`, `symbol="NVDA"`, `range_="1mo"`, `interval="1d"` |
| 3 | Tìm mã giao dịch của công ty Microsoft. | `market_data` | `action="search"`, `query="Microsoft"` |
| 4 | Phân tích nhóm ngành bán dẫn, tập trung vào NVDA và AMD. | `sector_analysis` | `sector="semiconductors"`, `tickers=["NVDA","AMD"]` |
| 5 | Phân tích nhóm ngành ngân hàng Việt Nam với VCB.VN và TCB.VN. | `sector_analysis` | `sector="banking"`, `tickers=["VCB.VN","TCB.VN"]`, `region="vietnam"` |
| 6 | Lấy 5 dòng dữ liệu lịch sử gần nhất của cổ phiếu HPG từ vnstock. | `vnstock_tool` | `symbol="HPG"`, `limit=5` |
| 7 | Kiểm tra mã FPT có tín hiệu cá voi gom/xả trong 30 phiên gần nhất không. | `whale_market_flow` | `symbol="FPT"`, `days=30` |
| 8 | Phân tích thanh khoản HPG, dùng ngưỡng volume đột biến 2 lần trung bình. | `whale_market_flow` | `symbol="HPG"`, `threshold_multiplier=2.0` |
| 9 | Tin AI hôm nay có gì nổi bật? | `lookup` | `query="AI"`, `topic="news"`, `timeframe="day"` |
| 10 | Tìm trên web tin OpenAI trong tuần này. | `lookup` | `query="OpenAI"`, `topic="news"`, `timeframe="week"` |
| 11 | Mọi người đang nói gì về NVDA trên Twitter? | `social_search` | `query="NVDA"`, `search_type="Latest"` |
| 12 | Cho mình các tweet phổ biến nhất về OpenAI. | `social_search` | `query="OpenAI"`, `search_type="Top"` |
| 13 | Lấy 3 tweet mới nhất của Elon Musk. | `timeline` | `screenname="elonmusk"`, `limit=3` |
| 14 | Tóm tắt bài này: https://openai.com/blog/gpt-5 | `fetch` | `url="https://openai.com/blog/gpt-5"` |
| 15 | Tìm trên web tin AI hôm nay và tìm thêm tweet về AI. | `lookup` + `social_search` | `lookup(query="AI", topic="news", timeframe="day")`, `social_search(query="AI")` |
| 16 | Tóm tắt 5 tweet mới nhất giúp mình. | `clarify` | `response_type="text"` |
| 17 | Tóm tắt bài viết này hộ mình. | `clarify` | `response_type="text"` |
| 18 | Đăng bản tin này lên Telegram giúp mình. | `clarify` | `response_type="yes_no"` |
| 19 | Bạn là gì và làm được gì? | no tool | answer directly |
| 20 | Viết hàm Python tính Fibonacci bằng recursion. | no tool | refuse/redirect as out of scope |

## Live Demo Flow

1. Chạy:

```powershell
python chat.py --provider openrouter --version v3
```

2. Dùng các câu hỏi 1, 4, 7, 15, 18 để demo nhiều loại tool:

- `market_data`: giá/lịch sử/tìm mã.
- `sector_analysis`: phân tích nhóm ngành.
- `whale_market_flow`: dòng tiền cá voi/thanh khoản.
- `lookup` + `social_search`: multi-tool.
- `clarify`: boundary trước khi gửi Telegram.

## Notes

- Các câu hỏi về `market_data` và `whale_market_flow` cần mạng để gọi Yahoo Finance public endpoint.
- `sector_analysis` gọi Alpha Vantage nếu có `ALPHAVANTAGE_API_KEY`; nếu không có key vẫn fallback static.
- `vnstock_tool` cần package `vnstock`; nếu chưa cài, tool trả structured error nhưng routing vẫn có thể pass.
