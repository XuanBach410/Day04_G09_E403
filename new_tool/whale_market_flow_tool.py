import json
import urllib.request
from datetime import datetime
from typing import Dict, Any

def fetch_market_flow_fallback(symbol: str, days: int = 30, threshold_multiplier: float = 2.0) -> Dict[str, Any]:
    """
    Phân tích dòng tiền cá voi & thanh khoản qua API chứng khoán công khai.
    """
    symbol = symbol.upper().strip()
    if not symbol:
        return {"error": "symbol_missing", "message": "Mã cổ phiếu không được để trống."}
    
    try:
        # Fallback thử dùng API vnstock nếu khả dụng
        try:
            from vnstock.api.quote import Quote
            stock = Quote(symbol=symbol, source='VCI')
            df = stock.history(start='2024-01-01', end='2024-12-31')
            if not df.empty:
                df = df.tail(max(days + 20, 50)).copy()
                df['vol_sma20'] = df['volume'].rolling(window=20).mean()
                df['vol_ratio'] = df['volume'] / df['vol_sma20']
                recent = df.tail(days)
                
                whale_events = []
                for idx, row in recent.iterrows():
                    ratio = float(row['vol_ratio']) if str(row['vol_ratio']) != 'nan' else 1.0
                    if ratio >= threshold_multiplier:
                        close_price = float(row['close'])
                        open_price = float(row['open'])
                        action = "Cá Voi Mua Gom mạnh (Đột biến + Giá Tăng)" if close_price > open_price else "Cá Voi Xả Hàng mạnh (Đột biến + Giá Giảm)"
                        change = round(((close_price - open_price) / open_price) * 100, 2) if open_price > 0 else 0.0
                        whale_events.append({
                            "date": str(row['time']) if 'time' in row else str(idx),
                            "volume": int(row['volume']),
                            "vol_vs_avg": round(ratio, 2),
                            "price_change_pct": change,
                            "signal": action
                        })
                
                latest_row = df.iloc[-1]
                latest_ratio = float(latest_row['vol_ratio']) if str(latest_row['vol_ratio']) != 'nan' else 1.0
                state = "ẢM ĐẠM / MUA BÁN ÍT" if latest_ratio < 0.6 else ("SÔI ĐỘNG TRỞ LẠI" if latest_ratio >= 1.5 else "BÌNH THƯỜNG")
                
                return {
                    "symbol": symbol,
                    "latest_price": float(latest_row['close']),
                    "latest_volume": int(latest_row['volume']),
                    "avg_volume_20d": int(latest_row['vol_sma20']) if str(latest_row['vol_sma20']) != 'nan' else 0,
                    "volume_ratio_vs_avg": round(latest_ratio, 2),
                    "market_liquidity_status": state,
                    "whale_alerts_count": len(whale_events),
                    "whale_detected_events": whale_events[-5:]
                }
        except Exception:
            pass

        # Nguồn dữ liệu fallback Yahoo Finance (Mã chứng khoán VN có hậu tố .VN)
        yf_symbol = f"{symbol}.VN" if not symbol.endswith(".VN") else symbol
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{yf_symbol}?range=3mo&interval=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        
        result = data['chart']['result'][0]
        timestamps = result['timestamp']
        quote = result['indicators']['quote'][0]
        closes = quote['close']
        opens = quote['open']
        volumes = quote['volume']
        
        records = []
        for t, o, c, v in zip(timestamps, opens, closes, volumes):
            if o is not None and c is not None and v is not None:
                records.append({
                    "date": datetime.fromtimestamp(t).strftime("%Y-%m-%d"),
                    "open": float(o),
                    "close": float(c),
                    "volume": int(v)
                })
        
        if not records:
            return {"error": "no_data", "message": f"Không lấy được dữ liệu thị trường cho mã {symbol}"}
        
        # Tính SMA20 Volume
        for i in range(len(records)):
            start_i = max(0, i - 19)
            v_subset = [r['volume'] for r in records[start_i:i+1]]
            sma20 = sum(v_subset) / len(v_subset)
            records[i]['vol_sma20'] = sma20
            records[i]['vol_ratio'] = records[i]['volume'] / sma20 if sma20 > 0 else 1.0

        recent_records = records[-days:]
        whale_events = []
        for r in recent_records:
            if r['vol_ratio'] >= threshold_multiplier:
                action = "Cá Voi Mua Gom mạnh (Đột biến + Giá Tăng)" if r['close'] > r['open'] else "Cá Voi Xả Hàng mạnh (Đột biến + Giá Giảm)"
                change = round(((r['close'] - r['open']) / r['open']) * 100, 2) if r['open'] > 0 else 0.0
                whale_events.append({
                    "date": r['date'],
                    "volume": r['volume'],
                    "vol_vs_avg": round(r['vol_ratio'], 2),
                    "price_change_pct": change,
                    "signal": action
                })
        
        latest = records[-1]
        latest_ratio = latest['vol_ratio']
        if latest_ratio < 0.6:
            state = "ẢM ĐẠM / MUA BÁN ÍT (Thanh khoản kiệt cược, nhà đầu tư đứng ngoài quan sát)"
        elif latest_ratio >= 1.5:
            state = "SÔI ĐỘNG TRỞ LẠI / DÒNG TIỀN VÀO MẠNH (Thanh khoản bùng nổ so với trung bình 20 phiên)"
        else:
            state = "TRUNG BÌNH / BÌNH THƯỜNG (Thanh khoản duy trì ở mức ổn định)"
            
        return {
            "symbol": symbol,
            "latest_price": round(latest['close'], 2),
            "latest_volume": latest['volume'],
            "avg_volume_20d": int(latest['vol_sma20']),
            "volume_ratio_vs_avg": round(latest_ratio, 2),
            "market_liquidity_status": state,
            "whale_alerts_count": len(whale_events),
            "whale_detected_events": whale_events[-5:]
        }
    except Exception as e:
        return {"error": type(e).__name__, "message": str(e)}

def execute(symbol: str = "", days: int = 30, threshold_multiplier: float = 2.0, **kwargs) -> Dict[str, Any]:
    if isinstance(symbol, dict):
        args = symbol
        symbol = args.get("symbol", "")
        days = args.get("days", 30)
        threshold_multiplier = args.get("threshold_multiplier", 2.0)
    return fetch_market_flow_fallback(symbol=symbol, days=days, threshold_multiplier=threshold_multiplier)

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    symbol = sys.argv[1] if len(sys.argv) > 1 else "HPG"
    print(json.dumps(execute(symbol=symbol), ensure_ascii=False, indent=2))
