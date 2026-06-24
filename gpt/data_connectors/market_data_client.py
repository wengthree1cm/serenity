from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from data_connectors.yahoo_client import extract_quote_snapshot, fetch_chart, fetch_quote_summary


def build_market_data_profile(
    ticker: str,
    cache_dir: str | Path = "data_cache",
) -> dict[str, Any]:
    symbol = ticker.upper().strip()
    warnings: list[str] = []
    endpoint_failures: list[str] = []
    source_urls = [
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
        f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}",
    ]

    chart_json: dict[str, Any] = {}
    quote_summary_json: dict[str, Any] = {}
    chart_snapshot: dict[str, Any] = {}
    quote_modules: dict[str, Any] = {}

    try:
        chart_json = fetch_chart(symbol, range="1y", interval="1d", cache_dir=cache_dir)
        chart_snapshot = extract_quote_snapshot(chart_json)
    except Exception as exc:
        endpoint_failures.append(f"Yahoo chart failed for {symbol}: {exc}")
        warnings.append(f"Yahoo chart unavailable for {symbol}.")

    try:
        quote_summary_json = fetch_quote_summary(symbol, cache_dir=cache_dir)
        result = ((quote_summary_json.get("quoteSummary") or {}).get("result") or [None])[0]
        if result:
            quote_modules = result
        else:
            error = (quote_summary_json.get("quoteSummary") or {}).get("error")
            endpoint_failures.append(f"Yahoo quoteSummary returned no result for {symbol}: {error}")
            warnings.append(f"Yahoo quoteSummary returned no result for {symbol}.")
    except Exception as exc:
        endpoint_failures.append(f"Yahoo quoteSummary failed for {symbol}: {exc}")
        warnings.append(f"Yahoo quoteSummary unavailable for {symbol}.")

    price_module = quote_modules.get("price") or {}
    summary_detail = quote_modules.get("summaryDetail") or {}
    key_stats = quote_modules.get("defaultKeyStatistics") or {}
    financial_data = quote_modules.get("financialData") or {}

    as_of = _as_of_date(price_module, chart_snapshot)

    current_price = _first_raw(
        financial_data.get("currentPrice"),
        price_module.get("regularMarketPrice"),
        chart_snapshot.get("current_price"),
    )
    previous_close = _first_raw(
        summary_detail.get("regularMarketPreviousClose"),
        summary_detail.get("previousClose"),
        price_module.get("regularMarketPreviousClose"),
        chart_snapshot.get("previous_close"),
    )
    shares = _first_raw(
        key_stats.get("sharesOutstanding"),
        key_stats.get("impliedSharesOutstanding"),
    )
    market_cap = _first_raw(
        price_module.get("marketCap"),
        summary_detail.get("marketCap"),
        summary_detail.get("nonDilutedMarketCap"),
    )
    market_cap_computed = False
    if market_cap is None and current_price is not None and shares is not None:
        market_cap = current_price * shares
        market_cap_computed = True

    enterprise_value = _first_raw(key_stats.get("enterpriseValue"))
    total_cash = _first_raw(financial_data.get("totalCash"))
    total_debt = _first_raw(financial_data.get("totalDebt"))
    net_debt = None
    if total_debt is not None and total_cash is not None:
        net_debt = total_debt - total_cash
    trailing_revenue = _first_raw(financial_data.get("totalRevenue"))
    gross_margin = _first_raw(financial_data.get("grossMargins"))
    free_cash_flow = _first_raw(financial_data.get("freeCashflow"))

    ev_to_sales = _first_raw(key_stats.get("enterpriseToRevenue"))
    ev_to_sales_computed = False
    if ev_to_sales is None and enterprise_value is not None and trailing_revenue:
        ev_to_sales = enterprise_value / trailing_revenue
        ev_to_sales_computed = True

    price_to_sales = _first_raw(
        summary_detail.get("priceToSalesTrailing12Months"),
        key_stats.get("priceToSalesTrailing12Months"),
    )
    price_to_sales_computed = False
    if price_to_sales is None and market_cap is not None and trailing_revenue:
        price_to_sales = market_cap / trailing_revenue
        price_to_sales_computed = True

    pe_ratio = _first_raw(summary_detail.get("trailingPE"), key_stats.get("trailingPE"))
    ev_to_ebitda = _first_raw(key_stats.get("enterpriseToEbitda"))
    high_52w = _first_raw(summary_detail.get("fiftyTwoWeekHigh"), chart_snapshot.get("fifty_two_week_high"))
    low_52w = _first_raw(summary_detail.get("fiftyTwoWeekLow"), chart_snapshot.get("fifty_two_week_low"))
    distance_high = None
    if current_price is not None and high_52w:
        distance_high = (current_price - high_52w) / high_52w
    distance_low = None
    if current_price is not None and low_52w:
        distance_low = (current_price - low_52w) / low_52w

    market_data = {
        "current_price": _field(current_price, _source("current_price", market_cap_computed=False), as_of),
        "previous_close": _field(previous_close, "yahoo_quote_summary.summaryDetail.previousClose", as_of),
        "market_cap": _field(
            market_cap,
            "computed" if market_cap_computed else "yahoo_quote_summary.price.marketCap",
            as_of,
            "medium" if market_cap_computed else "high",
            "current_price * shares_outstanding" if market_cap_computed else None,
        ),
        "shares_outstanding": _field(shares, "yahoo_quote_summary.defaultKeyStatistics.sharesOutstanding", as_of),
        "enterprise_value": _field(enterprise_value, "yahoo_quote_summary.defaultKeyStatistics.enterpriseValue", as_of),
        "total_cash": _field(total_cash, "yahoo_quote_summary.financialData.totalCash", as_of),
        "total_debt": _field(total_debt, "yahoo_quote_summary.financialData.totalDebt", as_of),
        "net_debt": _field(
            net_debt,
            "computed",
            as_of,
            "medium",
            "total_debt - total_cash" if net_debt is not None else None,
        ),
        "trailing_revenue": _field(trailing_revenue, "yahoo_quote_summary.financialData.totalRevenue", as_of),
        "revenue_ttm": _field(trailing_revenue, "yahoo_quote_summary.financialData.totalRevenue", as_of),
        "gross_margin": _field(gross_margin, "yahoo_quote_summary.financialData.grossMargins", as_of),
        "free_cash_flow": _field(free_cash_flow, "yahoo_quote_summary.financialData.freeCashflow", as_of),
        "ev_to_sales": _field(
            ev_to_sales,
            "computed" if ev_to_sales_computed else "yahoo_quote_summary.defaultKeyStatistics.enterpriseToRevenue",
            as_of,
            "medium" if ev_to_sales_computed else "high",
            "enterprise_value / trailing_revenue" if ev_to_sales_computed else None,
        ),
        "price_to_sales": _field(
            price_to_sales,
            "computed" if price_to_sales_computed else "yahoo_quote_summary.summaryDetail.priceToSalesTrailing12Months",
            as_of,
            "medium" if price_to_sales_computed else "high",
            "market_cap / trailing_revenue" if price_to_sales_computed else None,
        ),
        "pe_ratio": _field(pe_ratio, "yahoo_quote_summary.summaryDetail.trailingPE", as_of),
        "ev_to_ebitda": _field(ev_to_ebitda, "yahoo_quote_summary.defaultKeyStatistics.enterpriseToEbitda", as_of),
        "fifty_two_week_high": _field(high_52w, "yahoo_quote_summary.summaryDetail.fiftyTwoWeekHigh", as_of),
        "fifty_two_week_low": _field(low_52w, "yahoo_quote_summary.summaryDetail.fiftyTwoWeekLow", as_of),
        "price_change_1m": _field(chart_snapshot.get("price_change_1m"), "yahoo_chart.close_history", as_of, "medium"),
        "price_change_3m": _field(chart_snapshot.get("price_change_3m"), "yahoo_chart.close_history", as_of, "medium"),
        "price_change_6m": _field(chart_snapshot.get("price_change_6m"), "yahoo_chart.close_history", as_of, "medium"),
        "price_change_12m": _field(chart_snapshot.get("price_change_12m"), "yahoo_chart.close_history", as_of, "medium"),
        "distance_from_52w_high": _field(
            distance_high,
            "computed",
            as_of,
            "medium",
            "(current_price - 52_week_high) / 52_week_high" if distance_high is not None else None,
        ),
        "distance_from_52w_low": _field(
            distance_low,
            "computed",
            as_of,
            "medium",
            "(current_price - 52_week_low) / 52_week_low" if distance_low is not None else None,
        ),
    }

    missing_fields = [name for name, payload in market_data.items() if payload.get("value") is None]
    return {
        "ticker": symbol,
        "market_data": market_data,
        "financial_data": {
            key: market_data[key]
            for key in [
                "total_cash",
                "total_debt",
                "net_debt",
                "trailing_revenue",
                "revenue_ttm",
                "gross_margin",
                "free_cash_flow",
            ]
        },
        "source_urls": source_urls,
        "missing_fields": missing_fields,
        "data_quality_warnings": warnings,
        "endpoint_failures": endpoint_failures,
    }


def _field(
    value: Any,
    source: str,
    as_of_date: str | None,
    confidence: str = "high",
    computation_note: str | None = None,
) -> dict[str, Any]:
    return {
        "value": value,
        "source": source,
        "as_of_date": as_of_date,
        "confidence": confidence if value is not None else "low",
        "computation_note": computation_note,
    }


def _first_raw(*values: Any) -> Any:
    for value in values:
        raw = _raw(value)
        if raw is not None:
            return raw
    return None


def _raw(value: Any) -> Any:
    if isinstance(value, dict):
        return value.get("raw")
    return value


def _as_of_date(price_module: dict[str, Any], chart_snapshot: dict[str, Any]) -> str | None:
    raw_time = _raw(price_module.get("regularMarketTime"))
    if isinstance(raw_time, (int, float)):
        return datetime.fromtimestamp(raw_time, tz=timezone.utc).isoformat()
    timestamp = chart_snapshot.get("timestamp")
    return timestamp if isinstance(timestamp, str) else None


def _source(field_name: str, market_cap_computed: bool = False) -> str:
    if field_name == "current_price":
        return "yahoo_quote_summary.financialData.currentPrice"
    return "yahoo_quote_summary"
