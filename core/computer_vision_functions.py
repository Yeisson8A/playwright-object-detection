import cv2


def detect_objects(path, model):

    results = model(path)

    detections = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            label = model.names[cls]

            detections.append(label)

    return detections

def extract_text(path, reader):

    # cargar imagen
    img = cv2.imread(path)

    # ---- OPCION 2: ESCALAR IMAGEN ----
    scale = 2
    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # ---- OPCION 1: PREPROCESAMIENTO ----

    # escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # reducir ruido
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # mejorar contraste
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # EasyOCR espera imagen en RGB
    processed = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)

    # ---- OCR ----
    results = reader.readtext(processed)

    textos = []

    for bbox, text, conf in results:
        textos.append({
            "text": text,
            "confidence": conf
        })

    return textos