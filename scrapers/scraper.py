from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from constants.constants import BASE_URL
from core.computer_vision_functions import detect_objects, extract_text
from utils.utils import download_image

def scrape_books(download_dir, model, reader, max_books=10):

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/catalogue/category/books/science_22/index.html")

        page.wait_for_selector("article.product_pod")

        books = page.locator("article.product_pod h3 a")
        count = books.count()

        print("Libros detectados:", count)

        book_links = []

        # Obtener URLs primero
        for i in range(min(count, max_books)):
            href = books.nth(i).get_attribute("href")

            full_url = urljoin(page.url, href)

            book_links.append(full_url)

        # Entrar a cada libro
        for link in book_links:

            print("Procesando:", link)

            page.goto(link)

            page.wait_for_selector(".product_main h1")

            # 1️⃣ extraer título
            title = page.locator(".product_main h1").inner_text()

            # 2️⃣ obtener imagen HD
            img = page.locator(".item.active img")

            img_src = img.get_attribute("src")

            img_url = urljoin(BASE_URL, img_src)

            filename = img_url.split("/")[-1]

            save_path = download_dir / filename

            print("Descargando imagen:", img_url)

            download_image(img_url, save_path)

            results.append({
                "title": title,
                "image_url": img_url,
                "image": filename,
                "detections": detect_objects(save_path, model),
                "text": extract_text(save_path, reader)
            })

        browser.close()

    return results