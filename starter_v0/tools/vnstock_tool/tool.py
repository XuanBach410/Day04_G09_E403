from __future__ import annotations

from typing import Any

from tools._shared import err


def get_vnstock_history(symbol: str = "", start: str = "2024-01-01", end: str = "2024-12-31", limit: int = 5) -> dict[str, Any]:
    """Fetch recent Vietnam stock history through vnstock when the package is installed."""
    try:
        clean_symbol = symbol.strip().upper()
        if not clean_symbol:
            raise ValueError("symbol is required, for example HPG, FPT, VCB, SSI")

        from vnstock.api.quote import Quote

        stock = Quote(symbol=clean_symbol, source="VCI")
        df = stock.history(start=start, end=end)
        if df.empty:
            return {"tool": "vnstock_tool", "symbol": clean_symbol, "rows": [], "message": "No data returned from vnstock."}

        recent = df.tail(max(1, int(limit or 5))).copy()
        rows = recent.to_dict(orient="records")
        return {
            "tool": "vnstock_tool",
            "symbol": clean_symbol,
            "start": start,
            "end": end,
            "limit": limit,
            "rows": rows,
            "source": "vnstock VCI",
            "disclaimer": "Reference only, not investment advice.",
        }
    except Exception as exc:
        return err("vnstock_tool", exc)
