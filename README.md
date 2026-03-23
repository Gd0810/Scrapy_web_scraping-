# Web Scraper (Static + Dynamic)

A small Scrapy + Playwright project with a Streamlit UI. It can scrape both static HTML pages and JavaScript-rendered pages.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:

```bash
python -m playwright install
```

## Run the UI

```bash
streamlit run app.py
```

## How it works

- **Static mode** uses plain Scrapy (fast).
- **Dynamic mode** uses Scrapy + Playwright (for JS-rendered pages).
- **Auto mode** tries static first and falls back to dynamic if the content looks empty.
