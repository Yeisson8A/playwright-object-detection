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

def preprocess_image(path):

    path = str(path)
    img = cv2.imread(path)

    # convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # escalar imagen (muy importante para texto pequeño)
    scale = 2
    gray = cv2.resize(
        gray,
        None,
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_CUBIC
    )

    # mejorar contraste
    gray = cv2.equalizeHist(gray)

    return gray

def extract_text(path, pipeline):

    img = preprocess_image(path)

    # Keras OCR espera imagen en RGB
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    prediction_groups = pipeline.recognize([img])[0]

    # ordenar por posición (arriba → abajo, izquierda → derecha)
    prediction_sorted = sorted(
        prediction_groups,
        key=lambda x: (x[1][:,1].mean(), x[1][:,0].mean())
    )

    words = [text for text, box in prediction_sorted]

    return " ".join(words)