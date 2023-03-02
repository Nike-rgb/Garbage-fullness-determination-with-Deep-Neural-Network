from flask import Flask, request, render_template, send_file, jsonify
import tensorflow as tf
import pandas as pd
import logging
from flask_socketio import SocketIO, emit
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import schedule
import time
import threading
from datetime import datetime
import os
import csv
from lib.save_image import save_image
from lib.predict import predict
from schedules.incremental_learn import incremental_learn
from schedules.lstm_train import train_timeseries

app = Flask(__name__, template_folder='../Web application for monitoring/public',
static_url_path='/static', static_folder='../Web application for monitoring/public')
model = tf.keras.models.load_model('../model/fullness_determination_model.h5')
lstm_model = tf.keras.models.load_model('../model/lstm_model.h5')
socketio = SocketIO(app, async_mode='gevent')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

database = {
}

def updateDevices(id, latlng, label):
    if id not in database:
        database[id] = {
            "id": id,
            "latlng": latlng,
            "fullness": label
        }
    else:
        database[id]["latlng"] = latlng
        database[id]["fullness"] = label

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/activeDevices")
def sendActiveDevices():
    return jsonify(database)

@app.route("/getImagePaths")
def getImagePaths():
    id = request.args.get('id')
    dirPath = os.path.join('images', id)
    all_files = os.listdir(dirPath)
    sorted_files = sorted(all_files, key=lambda x: os.path.getctime(os.path.join(dirPath, x)), reverse=True)
    image_paths = sorted_files[:4]
    return jsonify(image_paths)

@app.route("/getImage")
def getImage():
    id = request.args.get('id')
    filename = request.args.get('filename')
    imagePath = os.path.join('images', id, filename)
    return send_file(imagePath, mimetype='image/jpeg')

def updateCsv(label):
    labels = ["empty", "full", "half-full"]
    today = datetime.now().strftime('%Y-%m-%d')
    timeseries_file = os.path.join("timeseries", f"timeseries_{today}.csv")
    if os.path.isfile(timeseries_file):
        with open(timeseries_file, 'a') as f:
            writer = csv.writer(f)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, labels.index(label)])
    else:
        with open(timeseries_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'label'])
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, labels.index(label)])

@app.route('/data', methods=['POST'])
def handle_data():
    try:
        if 'image' in request.files:
            image = request.files['image'].read()
            id = 'abcd'
            latlng = [27.694431940721817, 85.32002538442613]
            label = predict(model, image)
            savePath = os.path.join("images", id)
            save_image(image, savePath)
            updateCsv(label)
            updateDevices(id, latlng, label)
            socketio.emit("newDataAvailable", broadcast=True)
            return "OKAY"
        else:
            return 'Request failed', 500
    except Exception as e:
        log.error('Request failed: {}'.format(str(e)))
        return 'Request failed', 500

@socketio.on("connect")
def handle_connect():
    print("Hey a client has connected")

stop_event = threading.Event()
def schedule_cnn_incremental():
    schedule.every(2).minutes.do(lambda: incremental_learn(model))
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)

cnn_thread = threading.Thread(target=schedule_cnn_incremental)
cnn_thread.start()

import keyboard
def stop_scheduler():
    print("Stopping scheduler.")
    stop_event.set()

def check_keyboard():
    while True:
        try:
            if keyboard.is_pressed('q'):
                stop_scheduler()
                break
        except:
            break

keyboard_thread = threading.Thread(target=check_keyboard)
keyboard_thread.start()


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 3000), app, handler_class=WebSocketHandler)
    server.serve_forever()
