from urllib.parse import urljoin
from constants.constants import BASE_URL
from core.computer_vision_functions import detect_objects, extract_text
from utils.utils import download_image


async def scrape_book(browser, link, download_dir, model, pipeline):

    page = await browser.new_page()

    try:

        print("Procesando:", link)

        await page.goto(link)

        await page.wait_for_selector(".product_main h1")

        # título
        title = await page.locator(".product_main h1").inner_text()

        # imagen
        img = page.locator(".item.active img")
        img_src = await img.get_attribute("src")

        img_url = urljoin(BASE_URL, img_src)

        filename = img_url.split("/")[-1]
        save_path = download_dir / filename

        print("Descargando:", img_url)

        await download_image(img_url, save_path)

        detections = detect_objects(save_path, model)
        text = extract_text(save_path, pipeline)

        result = {
            "title": title,
            "image_url": img_url,
            "image": filename,
            "detections": detections,
            "text": text
        }

    except Exception as e:
        print("Error:", e)
        result = None

    await page.close()

    return result