import json
from typing import Dict, Any

def execute(args: Dict[str, Any]) -> str:
    """
    Thực thi việc lấy dữ liệu cổ phiếu qua vnstock.
    """
    symbol = args.get("symbol", "").upper()
    if not symbol:
        return "Lỗi: Tham số 'symbol' bị thiếu."

    print(f"\n[Tool Execution] Đang kéo dữ liệu thật cho mã {symbol} từ vnstock...")
    try:
        from vnstock import Vnstock
        stock = Vnstock().stock(symbol=symbol, source='TCBS')
        df = stock.quote.history(start='2024-01-01', end='2024-12-31') 
        recent_data = df.tail(5) 
        return recent_data.to_string()
    except Exception as e:
        return f"Lỗi khi lấy dữ liệu: {str(e)} ({type(e).__name__})"
