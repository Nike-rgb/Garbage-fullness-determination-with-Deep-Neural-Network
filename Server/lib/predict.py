import numpy as np
import cv2
from lib.save_image import save_image
import os

confidence_threshold = 0.8

def preprocess(image):
    np_image = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (100, 100))
    image = image.reshape(-1, 100, 100, 1)
    image = image / 255
    return image

def predict(model, image):
    path = "incremental_checkpoints/model_weights.h5"
    if(os.path.exists(path)):
        model.load_weights(path)
    processed_image = preprocess(image)
    prediction = model.predict(processed_image)
    prediction_dict = {"prediction": prediction.tolist()}
    print(prediction_dict)
    pred_label = np.argmax(prediction, axis=1)
    confidence = prediction[0, pred_label]
    label = ["empty", "full", "half-full"][pred_label[0]]
    if confidence >= confidence_threshold:
        path = os.path.join("Incremental dataset", label)
        save_image(image, path)
    return label