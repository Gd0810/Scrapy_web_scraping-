import streamlit as st
from run_spider import run_spider

st.set_page_config(page_title="Dynamic Web Scraper", layout="wide")

st.title("🕷️ Dynamic Web Scraper (Scrapy + Playwright)")

url = st.text_input("Enter Website URL")

if st.button("Scrape"):
    if url:
        with st.spinner("Scraping dynamic content..."):
            data = run_spider(url)

        st.success("Scraping Completed!")

        for item in data:
            st.subheader(item["title"])
            st.write(item["url"])
            st.code(item["content"])
    else:
        st.warning("Please enter a valid URL")