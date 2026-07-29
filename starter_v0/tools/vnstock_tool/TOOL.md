# vnstock_tool

Fetches recent historical data for Vietnamese stock tickers through the optional `vnstock` package.

Use this tool when the user explicitly asks for Vietnam stock market historical data, recent OHLCV rows, or VN tickers such as `HPG`, `FPT`, `VCB`, `SSI`.

Do not use this tool for US stocks, crypto, ETFs, general market data, sector analysis, or whale/liquidity signals.

Arguments:

- `symbol`: Vietnamese ticker, uppercase preferred, for example `HPG`, `FPT`, `VCB`.
- `start`: start date in `YYYY-MM-DD`.
- `end`: end date in `YYYY-MM-DD`.
- `limit`: number of recent rows to return.

This tool requires `vnstock` to be installed. If it is not installed, it returns a structured error instead of crashing.
