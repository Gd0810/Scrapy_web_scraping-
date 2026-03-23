import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def _fetch_static(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    html = resp.text or ""
    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""

    return {
        "title": title,
        "url": resp.url,
        "content": html[:2000],
        "mode": "static",
        "status": resp.status_code,
    }


def _fetch_dynamic(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        title = page.title()
        html = page.content() or ""
        browser.close()

    return {
        "title": title,
        "url": url,
        "content": html[:2000],
        "mode": "dynamic",
    }


def run_spider(url, mode="auto"):
    if mode == "static":
        return [_fetch_static(url)]
    if mode == "dynamic":
        return [_fetch_dynamic(url)]

    # Auto: try static first, fall back to dynamic if content looks empty
    static_item = _fetch_static(url)
    if len(static_item.get("content") or "") >= 200:
        return [static_item]

    return [_fetch_dynamic(url)]
