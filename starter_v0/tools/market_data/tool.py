from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from tools._shared import err


BASE_URL = "https://query1.finance.yahoo.com"
USER_AGENT = "MarketDataTool/1.0 (educational use)"
VALID_INTERVALS = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"}
VALID_RANGES = {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"}


class MarketDataError(RuntimeError):
    pass


def _request_json(path: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise MarketDataError(f"Yahoo Finance returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise MarketDataError(f"Cannot connect to market data source: {exc.reason}") from exc
    except (TimeoutError, json.JSONDecodeError) as exc:
        raise MarketDataError(f"Invalid or timed-out market data response: {exc}") from exc


def _chart(symbol: str, range_: str, interval: str) -> dict[str, Any]:
    symbol = symbol.strip().upper()
    if not symbol:
        raise MarketDataError("symbol is required, for example AAPL, MSFT, BTC-USD or VNM.VN.")
    if range_ not in VALID_RANGES:
        raise MarketDataError(f"Invalid range: {range_}.")
    if interval not in VALID_INTERVALS:
        raise MarketDataError(f"Invalid interval: {interval}.")
    payload = _request_json(f"/v8/finance/chart/{quote(symbol)}", {"range": range_, "interval": interval})
    result = (payload.get("chart") or {}).get("result") or []
    if not result:
        error = (payload.get("chart") or {}).get("error") or {}
        raise MarketDataError(error.get("description") or f"Symbol not found: {symbol}.")
    return result[0]


def quote_price(symbol: str) -> dict[str, Any]:
    result = _chart(symbol, "1d", "1m")
    meta = result.get("meta") or {}
    market_time = meta.get("regularMarketTime")
    return {
        "symbol": meta.get("symbol", symbol.upper()),
        "short_name": meta.get("shortName") or meta.get("longName") or "",
        "price": meta.get("regularMarketPrice") or meta.get("previousClose"),
        "previous_close": meta.get("previousClose") or meta.get("chartPreviousClose"),
        "currency": meta.get("currency") or "",
        "exchange": meta.get("exchangeName") or "",
        "market_state": meta.get("marketState") or "",
        "as_of": datetime.fromtimestamp(market_time, tz=timezone.utc).isoformat() if market_time else None,
        "source": "Yahoo Finance public chart endpoint",
        "disclaimer": "Reference only, not investment advice.",
    }


def price_history(symbol: str, range_: str = "1mo", interval: str = "1d") -> dict[str, Any]:
    result = _chart(symbol, range_, interval)
    timestamps = result.get("timestamp") or []
    quote_data = ((result.get("indicators") or {}).get("quote") or [{}])[0]
    rows = []
    for index, timestamp in enumerate(timestamps):
        row = {"timestamp": datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()}
        for field in ("open", "high", "low", "close", "volume"):
            values = quote_data.get(field) or []
            row[field] = values[index] if index < len(values) else None
        rows.append(row)
    return {
        "symbol": (result.get("meta") or {}).get("symbol", symbol.upper()),
        "range": range_,
        "interval": interval,
        "rows": rows,
        "source": "Yahoo Finance public chart endpoint",
        "disclaimer": "Reference only, not investment advice.",
    }


def search_symbols(query: str, limit: int = 8) -> dict[str, Any]:
    query = query.strip()
    if not query:
        raise MarketDataError("query is required.")
    limit = max(1, min(int(limit), 20))
    payload = _request_json("/v1/finance/search", {"q": query, "quotesCount": str(limit), "newsCount": "0"})
    return {
        "query": query,
        "results": [
            {
                "symbol": item.get("symbol"),
                "name": item.get("shortname") or item.get("longname") or item.get("name"),
                "type": item.get("quoteType"),
                "exchange": item.get("exchDisp") or item.get("exchange"),
            }
            for item in (payload.get("quotes") or [])[:limit]
        ],
        "source": "Yahoo Finance public search endpoint",
    }


def market_data(action: str, symbol: str = "", range_: str = "1mo", interval: str = "1d", query: str = "", limit: int = 8) -> dict[str, Any]:
    try:
        action = action.strip().lower()
        if action == "quote":
            return quote_price(symbol)
        if action == "history":
            return price_history(symbol, range_, interval)
        if action == "search":
            return search_symbols(query, limit)
        raise MarketDataError("action must be quote, history, or search.")
    except Exception as exc:
        return err("market_data", exc)
