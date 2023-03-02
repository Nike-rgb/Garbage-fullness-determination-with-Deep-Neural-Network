import os
import datetime

def save_image(image, path):
    if not os.path.exists(path):
        os.makedirs(path)
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(path, f"image_{timestamp}.jpg")
    with open(filename, "wb") as f:
        f.write(image)