# Tool: Whale Market Flow (Cá voi & Phân tích Thanh khoản)

## Mô tả
Tool `whale_market_flow` giúp agent nhận biết dòng tiền đột biến từ các tổ chức/cá voi (Whale Flow) và tình trạng thanh khoản thị trường (ảm đạm vs sôi động trở lại) dựa trên khối lượng giao dịch so với trung bình 20 phiên.

## Đầu vào (Parameters)
- `symbol`: Mã cổ phiếu (ví dụ: `VNM`, `HPG`, `FPT`).
- `days`: Số phiên giao dịch lịch sử gần nhất để lọc tín hiệu (mặc định 30 ngày).
- `threshold_multiplier`: Hệ số bùng nổ khối lượng so với trung bình 20 phiên để phát hiện Cá Voi (mặc định 2.0x).

## Đầu ra (Returns)
Trả về JSON chứa thông tin:
- `market_liquidity_status`: Trạng thái thanh khoản hiện tại (`ẢM ĐẠM / MUA BÁN ÍT`, `SÔI ĐỘNG TRỞ LẠI`, `TRUNG BÌNH`).
- `volume_ratio_vs_avg`: Tỷ lệ khối lượng phiên mới nhất so với SMA(20).
- `whale_alerts_count`: Số phiên xuất hiện tín hiệu Cá Voi mua/bán gom.
- `whale_detected_events`: Chi tiết các phiên bùng nổ khối lượng kèm biến động giá.
