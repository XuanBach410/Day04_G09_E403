# sector_analysis

Analyzes a stock sector or a list of stock tickers using Alpha Vantage company overview API data plus a local sector knowledge base.

Use this tool when the user asks to analyze an industry group, compare tickers by sector, identify representative companies, summarize sector catalysts/risks, or build a watchlist by industry.

Do not use this tool for latest prices, latest news, social sentiment, or URL reading. Use the appropriate price/news/social/fetch tool for those requests.

Arguments:

- `sector`: optional sector name such as `technology`, `semiconductors`, `banking`, `energy`, `healthcare`, `consumer`, `real_estate`, `materials`, or Vietnamese equivalents.
- `tickers`: optional list of ticker symbols such as `AAPL`, `MSFT`, `NVDA`, `VCB.VN`.
- `region`: `global`, `us`, or `vietnam`.
- `detail_level`: `brief`, `standard`, or `deep`.
- `use_live_api`: whether to call Alpha Vantage for ticker profile fields such as sector, industry, market cap, beta, and P/E. Defaults to true. Requires `ALPHAVANTAGE_API_KEY` in `.env`.

At least one of `sector` or `tickers` should be provided.
