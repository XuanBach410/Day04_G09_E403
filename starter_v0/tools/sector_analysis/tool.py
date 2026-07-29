from __future__ import annotations

import os
import re
from typing import Any

import requests

from tools._shared import TIMEOUT, err, fold_text


ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"
HEADERS = {"User-Agent": "Mozilla/5.0"}


SECTORS: dict[str, dict[str, Any]] = {
    "technology": {
        "aliases": ["tech", "cong nghe", "công nghệ", "phan mem", "software"],
        "representative_tickers": ["AAPL", "MSFT", "GOOGL", "META", "ORCL", "CRM"],
        "drivers": ["AI adoption", "cloud spending", "enterprise software budgets", "consumer device cycles"],
        "risks": ["valuation compression", "regulation", "slower IT budgets", "platform competition"],
        "research_angles": ["revenue growth", "gross margin trend", "AI capex efficiency", "free cash flow"],
    },
    "semiconductors": {
        "aliases": ["chip", "chips", "ban dan", "bán dẫn", "semiconductor", "semis"],
        "representative_tickers": ["NVDA", "AMD", "INTC", "AVGO", "TSM", "ASML", "MU"],
        "drivers": ["AI accelerator demand", "data-center capex", "memory pricing", "foundry utilization"],
        "risks": ["export controls", "cyclical inventory corrections", "customer concentration", "capex digestion"],
        "research_angles": ["backlog", "data-center revenue", "gross margin", "supply constraints"],
    },
    "banking": {
        "aliases": ["bank", "banks", "ngan hang", "ngân hàng", "financials", "tai chinh", "tài chính"],
        "representative_tickers": ["JPM", "BAC", "WFC", "C", "VCB.VN", "TCB.VN", "BID.VN"],
        "drivers": ["net interest margin", "credit growth", "fee income", "capital adequacy"],
        "risks": ["non-performing loans", "rate cuts", "deposit competition", "regulatory pressure"],
        "research_angles": ["NIM", "NPL ratio", "loan growth", "CASA/deposit mix"],
    },
    "energy": {
        "aliases": ["oil", "gas", "dau khi", "dầu khí", "nang luong", "năng lượng"],
        "representative_tickers": ["XOM", "CVX", "COP", "SLB", "PVD.VN", "GAS.VN"],
        "drivers": ["oil prices", "gas demand", "OPEC supply policy", "refining margins"],
        "risks": ["commodity price volatility", "transition policy", "geopolitical shocks", "capex overruns"],
        "research_angles": ["realized prices", "production growth", "reserve replacement", "dividend coverage"],
    },
    "healthcare": {
        "aliases": ["health", "y te", "y tế", "pharma", "duoc", "dược"],
        "representative_tickers": ["LLY", "UNH", "JNJ", "PFE", "MRK", "DHG.VN"],
        "drivers": ["drug pipeline", "patent cycles", "insurance enrollment", "pricing power"],
        "risks": ["trial failures", "patent cliffs", "drug pricing regulation", "reimbursement pressure"],
        "research_angles": ["pipeline milestones", "approval dates", "loss-of-exclusivity exposure", "margin trend"],
    },
    "consumer": {
        "aliases": ["retail", "consumer", "tieu dung", "tiêu dùng", "ban le", "bán lẻ"],
        "representative_tickers": ["AMZN", "WMT", "COST", "NKE", "MWG.VN", "VNM.VN", "MSN.VN"],
        "drivers": ["consumer spending", "same-store sales", "brand strength", "e-commerce penetration"],
        "risks": ["weak demand", "inventory markdowns", "input cost inflation", "margin pressure"],
        "research_angles": ["same-store sales", "basket size", "inventory turnover", "operating margin"],
    },
    "real_estate": {
        "aliases": ["real estate", "property", "bat dong san", "bất động sản", "reit"],
        "representative_tickers": ["PLD", "AMT", "SPG", "VIC.VN", "VHM.VN", "NVL.VN"],
        "drivers": ["interest rates", "occupancy", "rental growth", "project handovers"],
        "risks": ["high leverage", "slow sales", "refinancing pressure", "policy delays"],
        "research_angles": ["debt maturity", "presales", "occupancy", "cash collection"],
    },
    "materials": {
        "aliases": ["materials", "steel", "hoa chat", "hóa chất", "thep", "thép"],
        "representative_tickers": ["LIN", "NEM", "FCX", "HPG.VN", "HSG.VN", "DGC.VN"],
        "drivers": ["commodity demand", "China construction cycle", "input prices", "export demand"],
        "risks": ["cyclical downturn", "oversupply", "energy costs", "trade barriers"],
        "research_angles": ["selling price", "capacity utilization", "inventory levels", "EBITDA margin"],
    },
}

TICKER_TO_SECTOR = {
    ticker: sector
    for sector, data in SECTORS.items()
    for ticker in data["representative_tickers"]
}


def _normalize_sector(value: str) -> str | None:
    folded = fold_text(value)
    for sector, data in SECTORS.items():
        candidates = [sector, *data["aliases"]]
        if any(fold_text(candidate) in folded or folded in fold_text(candidate) for candidate in candidates):
            return sector
    return None


def _clean_tickers(tickers: list[str] | str | None) -> list[str]:
    if not tickers:
        return []
    if isinstance(tickers, str):
        tickers = tickers.replace(";", ",").split(",")
    return [str(ticker).strip().upper() for ticker in tickers if str(ticker).strip()]


def _raw(value: Any) -> Any:
    if isinstance(value, dict) and "raw" in value:
        return value["raw"]
    if isinstance(value, dict) and "fmt" in value:
        return value["fmt"]
    return value


def _fetch_alpha_vantage_overview(ticker: str, api_key: str) -> dict[str, Any]:
    response = requests.get(
        ALPHA_VANTAGE_URL,
        params={"function": "OVERVIEW", "symbol": ticker, "apikey": api_key},
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    data = response.json()
    if data.get("Note") or data.get("Information") or data.get("Error Message"):
        raise RuntimeError(data.get("Note") or data.get("Information") or data.get("Error Message"))
    if not data or not data.get("Symbol"):
        raise RuntimeError("Alpha Vantage returned no company overview")
    return {
        "ticker": ticker,
        "long_name": data.get("Name"),
        "exchange": data.get("Exchange"),
        "currency": data.get("Currency"),
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "country": data.get("Country"),
        "market_cap": data.get("MarketCapitalization"),
        "beta": data.get("Beta"),
        "trailing_pe": data.get("PERatio"),
        "forward_pe": data.get("ForwardPE"),
        "profit_margin": data.get("ProfitMargin"),
        "revenue_ttm": data.get("RevenueTTM"),
        "description": data.get("Description"),
        "source": "Alpha Vantage OVERVIEW API",
    }


def _fetch_api_profiles(tickers: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    profiles: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    api_key = os.getenv("ALPHAVANTAGE_API_KEY") or os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return profiles, [{"ticker": ",".join(tickers), "error": "MissingApiKey", "message": "Set ALPHAVANTAGE_API_KEY in .env to enable live sector API calls."}]
    for ticker in tickers:
        try:
            profiles.append(_fetch_alpha_vantage_overview(ticker, api_key))
        except Exception as exc:
            errors.append({"ticker": ticker, "error": type(exc).__name__, "message": _redact_secret(str(exc))})
    return profiles, errors


def _redact_secret(message: str) -> str:
    return re.sub(r"(?i)(apikey=)[^&\s)'\"]+", r"\1REDACTED", message)


def _sector_from_api(profiles: list[dict[str, Any]]) -> str | None:
    # Industry is usually more specific than broad sector. For example,
    # Alpha Vantage returns NVDA sector=TECHNOLOGY and industry=SEMICONDUCTORS;
    # the useful industry group for this lab is semiconductors.
    industry_text = " ".join(str(profile.get("industry")) for profile in profiles if profile.get("industry"))
    normalized = _normalize_sector(industry_text) if industry_text else None
    if normalized:
        return normalized

    sector_text = " ".join(str(profile.get("sector")) for profile in profiles if profile.get("sector"))
    return _normalize_sector(sector_text) if sector_text else None


def analyze_sector(
    sector: str = "",
    tickers: list[str] | str | None = None,
    region: str = "global",
    detail_level: str = "standard",
    use_live_api: bool = True,
) -> dict[str, Any]:
    try:
        clean_tickers = _clean_tickers(tickers)
        api_profiles: list[dict[str, Any]] = []
        api_errors: list[dict[str, str]] = []
        if use_live_api and clean_tickers:
            api_profiles, api_errors = _fetch_api_profiles(clean_tickers)

        normalized_sector = _normalize_sector(sector) if sector else None
        if not normalized_sector and api_profiles:
            normalized_sector = _sector_from_api(api_profiles)
        inferred_sectors = sorted({TICKER_TO_SECTOR[ticker] for ticker in clean_tickers if ticker in TICKER_TO_SECTOR})

        if not normalized_sector and inferred_sectors:
            normalized_sector = inferred_sectors[0]
        if not normalized_sector:
            return {
                "tool": "sector_analysis",
                "error": "missing_or_unknown_sector",
                "message": "Provide a known sector or representative ticker list.",
                "known_sectors": sorted(SECTORS),
                "api_profiles": api_profiles,
                "api_errors": api_errors,
            }

        data = SECTORS[normalized_sector]
        ticker_breakdown = [
            {
                "ticker": ticker,
                "matched_sector": TICKER_TO_SECTOR.get(ticker, "unknown"),
                "in_requested_sector": TICKER_TO_SECTOR.get(ticker) == normalized_sector,
            }
            for ticker in clean_tickers
        ]

        result: dict[str, Any] = {
            "tool": "sector_analysis",
            "sector": normalized_sector,
            "region": region,
            "detail_level": detail_level,
            "representative_tickers": data["representative_tickers"],
            "ticker_breakdown": ticker_breakdown,
            "api_profiles": api_profiles,
            "api_errors": api_errors,
            "drivers": data["drivers"],
            "risks": data["risks"],
            "research_angles": data["research_angles"],
            "suggested_followup_tools": [
                {"tool": "lookup", "when": "Need latest sector news or catalysts"},
                {"tool": "social_search", "when": "Need market/social sentiment"},
                {"tool": "format", "when": "Need a markdown digest after collecting items"},
            ],
            "note": "Combines Alpha Vantage company overview API data when ALPHAVANTAGE_API_KEY is set with a static sector knowledge base. Use lookup for latest news.",
        }

        if detail_level == "brief":
            result["drivers"] = result["drivers"][:2]
            result["risks"] = result["risks"][:2]
            result["research_angles"] = result["research_angles"][:2]
        return result
    except Exception as exc:
        return err("sector_analysis", exc)
