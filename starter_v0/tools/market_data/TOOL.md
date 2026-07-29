# market_data

Tra cứu dữ liệu thị trường công khai tương tự một phần `yfinance`.

Use this tool when the user asks for:

- latest/near-latest quote for a symbol;
- OHLCV price history;
- symbol lookup/search by company name, crypto, ETF, or index.

Do not use this tool for:

- sector/industry analysis; use `sector_analysis`;
- Vietnamese vnstock-specific history; use `vnstock_tool` when the user explicitly asks for Vietnam stock data;
- whale/liquidity flow signals; use `whale_market_flow`;
- news explanation; use `lookup`.

Arguments:

- `action`: `quote`, `history`, or `search`.
- `symbol`: ticker, for example `AAPL`, `BTC-USD`, `VNM.VN`. Required for `quote` and `history`.
- `range_`: history range such as `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `ytd`, `max`.
- `interval`: interval such as `1m`, `1h`, `1d`, `1wk`, `1mo`.
- `query`: search query. Required for `search`.
- `limit`: max search results.
