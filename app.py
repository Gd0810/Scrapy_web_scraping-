import asyncio
import sys
import streamlit as st

# Playwright needs the selector event loop on Windows to launch subprocesses.
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from run_spider import run_spider

st.title("Web Scraper (Static + Dynamic)")

url = st.text_input("Enter URL")
mode = st.selectbox("Mode", ["auto", "static", "dynamic"], index=0)

if st.button("Scrape"):
    if url:
        with st.spinner("Scraping content..."):
            try:
                data = run_spider(url, mode=mode)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        if data:
            st.success("Data fetched")

            for item in data:
                st.subheader(item.get("title") or "(no title)")
                st.write(item.get("url"))
                st.write(f"Mode: {item.get('mode', 'unknown')}")

                with st.expander("HTML Content"):
                    st.code(item.get("content") or "")
        else:
            st.warning("No data found")
