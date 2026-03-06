import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from constants.constants import BASE_URL
from scrapers.scraper_book import scrape_book

async def scrape_books(download_dir, model, pipeline, max_books=10):

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        await page.goto(f"{BASE_URL}/catalogue/category/books/science_22/index.html")

        await page.wait_for_selector("article.product_pod")

        books = page.locator("article.product_pod h3 a")

        count = await books.count()

        print("Libros detectados:", count)

        book_links = []

        for i in range(min(count, max_books)):

            href = await books.nth(i).get_attribute("href")

            full_url = urljoin(page.url, href)

            book_links.append(full_url)

        await page.close()

        tasks = []

        for link in book_links:

            tasks.append(
                scrape_book(browser, link, download_dir, model, pipeline)
            )

        results = await asyncio.gather(*tasks)

        await browser.close()

        return [r for r in results if r]