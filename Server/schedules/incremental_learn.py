import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint
import datetime
import os
import shutil

datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=120,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

dataset_dir = "Incremental dataset for CNN"

def incremental_learn(model):
    train_data = datagen.flow_from_directory(
    dataset_dir,
    target_size=(100, 100),
    batch_size=20,
    class_mode='sparse',
    color_mode='grayscale',
    subset='training')

    val_data = datagen.flow_from_directory(
    dataset_dir,
    target_size=(100, 100),
    batch_size=20,
    class_mode='sparse',
    color_mode="grayscale",
    subset='validation')

    if(len(train_data) != 0):
        checkpoint = ModelCheckpoint('increment_checkpoints/model_weights.h5', save_weights_only=True, save_best_only=False, verbose = 1)
        model.fit(train_data, validation_data=val_data, epochs=1, callbacks=[checkpoint])
        model.save("../model/model.h5")
        for subdir in os.listdir(dataset_dir):
            subdir_path = os.path.join(dataset_dir, subdir)
            if os.path.isdir(subdir_path):
                shutil.rmtree(subdir_path)
        now = datetime.datetime.now()
        print(now)
        print("Incremental learn complete")
    else:
        now = datetime.datetime.now()
        print(now)
        print("No new data to increment learn")

