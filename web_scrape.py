import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from playwright.async_api import async_playwright

import asyncio

client = OpenAI()

# -----------------------------
# Fetch static page text
# -----------------------------
def get_static_page_text(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return "\n".join(paragraphs)
    except Exception as e:
        return f"ERROR_FETCHING_STATIC_PAGE: {str(e)}"

# -----------------------------
# Fetch JS-heavy page text using async Playwright
# -----------------------------
async def get_js_page_text_async(url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=20000)
            await page.wait_for_load_state("networkidle")
            text = await page.inner_text("body")
            await browser.close()
            return text
    except Exception as e:
        return f"ERROR_FETCHING_JS_PAGE: {str(e)}"

# -----------------------------
# Fetch page text: static first, fallback to JS
# -----------------------------
async def fetch_page_text(url: str) -> str:
    text = get_static_page_text(url)
    if text.startswith("ERROR") or len(text.strip()) < 100:
        text = await get_js_page_text_async(url)
    return text

# -----------------------------
# Scrape a single URL
# -----------------------------
async def scrape_single_url(url: str):
    page_text = await fetch_page_text(url)

    if page_text.startswith("ERROR"):
        return {"url": url, "success": False, "error": page_text}

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a web data extractor.
Here is the content of a webpage:

{page_text}

Please extract structured data:
- Title
- Headings
- Summary
- Important Links
- Tables (if any)
- Contact info (email, phone)

Return as JSON.
"""
                }
            ]
        )

        extracted_data = response.choices[0].message.content

        return {"url": url, "success": True, "data": extracted_data}

    except Exception as e:
        return {"url": url, "success": False, "error": str(e)}

# -----------------------------
# Scrape multiple URLs in parallel
# -----------------------------
async def scrape_multiple_urls(urls: list[str]):
    tasks = [scrape_single_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return {"success": True, "count": len(results), "results": results}
