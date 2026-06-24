from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
YAHOO_CRUMB_URL = "https://query1.finance.yahoo.com/v1/test/getcrumb"
YAHOO_FC_URL = "https://fc.yahoo.com"
YAHOO_QUOTE_SUMMARY_URL = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
DEFAULT_CACHE_DIR = Path("data_cache")


def fetch_chart(
    ticker: str,
    range: str = "1y",
    interval: str = "1d",
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
) -> dict[str, Any]:
    symbol = ticker.upper().strip()
    url = YAHOO_CHART_URL.format(ticker=symbol)
    params = {"range": range, "interval": interval}
    headers = {"User-Agent": "Mozilla/5.0 serenity-research/0.1"}
    response = requests.get(url, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()
    _save_raw_response(cache_dir, symbol, "chart", response.url, data)
    return data


def fetch_quote_summary(
    ticker: str,
    modules: str = "price,summaryDetail,defaultKeyStatistics,financialData",
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
) -> dict[str, Any]:
    symbol = ticker.upper().strip()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 serenity-research/0.1"})
    session.get(YAHOO_FC_URL, timeout=20)
    crumb_response = session.get(YAHOO_CRUMB_URL, timeout=20)
    crumb_response.raise_for_status()
    crumb = crumb_response.text.strip()
    response = session.get(
        YAHOO_QUOTE_SUMMARY_URL.format(ticker=symbol),
        params={"modules": modules, "crumb": crumb},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    _save_raw_response(cache_dir, symbol, "quote_summary", response.url, data)
    return data


def extract_quote_snapshot(chart_json: dict[str, Any]) -> dict[str, Any]:
    result = ((chart_json.get("chart") or {}).get("result") or [None])[0]
    if not result:
        return {
            "ticker": None,
            "data_quality_warnings": ["Yahoo chart response did not include a result payload."],
        }

    meta = result.get("meta") or {}
    timestamps = result.get("timestamp") or []
    quote = (((result.get("indicators") or {}).get("quote") or [{}])[0]) or {}
    closes = quote.get("close") or []
    current_price = meta.get("regularMarketPrice")
    if current_price is None:
        current_price = _last_number(closes)

    snapshot = {
        "ticker": meta.get("symbol"),
        "exchange": meta.get("fullExchangeName") or meta.get("exchangeName"),
        "currency": meta.get("currency"),
        "current_price": current_price,
        "previous_close": meta.get("chartPreviousClose") or meta.get("previousClose"),
        "fifty_two_week_high": meta.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": meta.get("fiftyTwoWeekLow"),
        "market_cap": meta.get("marketCap"),
        "timestamp": _timestamp_to_iso(meta.get("regularMarketTime") or _last_number(timestamps)),
        "price_change_1m": _period_change(timestamps, closes, current_price, 30),
        "price_change_3m": _period_change(timestamps, closes, current_price, 90),
        "price_change_6m": _period_change(timestamps, closes, current_price, 180),
        "price_change_12m": _period_change(timestamps, closes, current_price, 365),
    }
    snapshot["missing_fields"] = [key for key, value in snapshot.items() if value is None]
    return snapshot


def _period_change(
    timestamps: list[int],
    closes: list[float | None],
    current_price: float | None,
    days_back: int,
) -> float | None:
    if not timestamps or not closes or current_price is None:
        return None

    target_ts = int(datetime.now(timezone.utc).timestamp()) - days_back * 24 * 60 * 60
    candidates = [
        (abs(ts - target_ts), close)
        for ts, close in zip(timestamps, closes)
        if isinstance(close, (int, float)) and ts <= target_ts + 7 * 24 * 60 * 60
    ]
    if not candidates:
        return None
    _, start_price = min(candidates, key=lambda item: item[0])
    if not start_price:
        return None
    return round((current_price - start_price) / start_price, 6)


def _last_number(values: list[Any]) -> Any:
    for value in reversed(values):
        if isinstance(value, (int, float)):
            return value
    return None


def _timestamp_to_iso(value: Any) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()


def _save_raw_response(
    cache_dir: str | Path,
    ticker: str,
    stem: str,
    url: str,
    data: dict[str, Any],
) -> None:
    folder = Path(cache_dir) / "yahoo" / ticker.upper()
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = folder / f"{timestamp}_{stem}.json"
    payload = {
        "source_url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
