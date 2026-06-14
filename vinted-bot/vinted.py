import time
import random
import requests

CATALOG_URL = "https://www.vinted.nl/api/v2/catalog/items"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
    "Referer": "https://www.vinted.nl/",
}

_session = requests.Session()
_session.headers.update(HEADERS)
_session_initialized = False


def _init_session() -> None:
    """Visit the Vinted homepage to acquire session cookies before API calls."""
    global _session_initialized
    if _session_initialized:
        return
    print("[vinted] initialising session (fetching cookies)...")
    try:
        _session.get("https://www.vinted.nl/", timeout=15)
        _session_initialized = True
        time.sleep(random.uniform(1, 2))
    except requests.RequestException as exc:
        print(f"[vinted] session init warning: {exc}")


def _get_with_backoff(url: str, params: dict, max_retries: int = 4) -> dict:
    _init_session()
    delay = 2.0
    for attempt in range(max_retries):
        try:
            resp = _session.get(url, params=params, timeout=15)
            if resp.status_code == 401:
                # Session expired — reinitialise cookies and retry once
                global _session_initialized
                _session_initialized = False
                _init_session()
                resp = _session.get(url, params=params, timeout=15)
            if resp.status_code == 429:
                wait = delay + random.uniform(0, delay * 0.5)
                print(f"[vinted] rate limited, waiting {wait:.1f}s (attempt {attempt + 1})")
                time.sleep(wait)
                delay *= 2
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            if attempt == max_retries - 1:
                raise
            wait = delay + random.uniform(0, 1)
            print(f"[vinted] request error: {exc}, retrying in {wait:.1f}s")
            time.sleep(wait)
            delay *= 2
    return {}


def search_multi(queries: list[str]) -> list[dict]:
    """Run multiple keyword queries and return deduplicated listings."""
    seen_ids: set[str] = set()
    results: list[dict] = []
    for query in queries:
        print(f"[vinted] querying: {query!r}")
        params = {
            "search_text": query,
            "order": "newest_first",
            "per_page": 96,
        }
        try:
            data = _get_with_backoff(CATALOG_URL, params)
        except requests.RequestException as exc:
            print(f"[vinted] query failed, skipping: {exc}")
            continue
        for item in data.get("items", []):
            parsed = _parse(item)
            if parsed["id"] and parsed["id"] not in seen_ids:
                seen_ids.add(parsed["id"])
                results.append(parsed)
        time.sleep(random.uniform(2, 5))
    return results


def _parse(item: dict) -> dict:
    return {
        "id": str(item.get("id", "")),
        "title": item.get("title", ""),
        "price": float(item.get("price", {}).get("amount", 0)),
        "currency": item.get("price", {}).get("currency_code", "EUR"),
        "condition": item.get("status", ""),
        "description": item.get("description", ""),
        "url": item.get("url", ""),
    }
