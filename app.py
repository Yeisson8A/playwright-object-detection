import easyocr
from ultralytics import YOLO
from scrapers.scraper import scrape_books
from utils.utils import create_download_folder, generate_report_json


if __name__ == "__main__":
    # Crear u obtener directorio para descarga de archivos
    download_dir = create_download_folder()
    # Configurar modelo para computer vision
    model = YOLO('./models/yolo11n.pt', task='detect')
    # inicializar OCR una sola vez (muy importante para performance)
    reader = easyocr.Reader(['en'], gpu=False)
    # Llamar función para hacer scraping y descargar archivos
    data = scrape_books(download_dir, model, reader)
    # Generar reporte JSON con los datos obtenidos
    generate_report_json(data, download_dir, "detections.json")
    print("Proceso finalizado. Reporte generado.")