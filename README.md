# Smart-Garbage-Monitoring-with-CNN-and-Gas-sensor

## Introduction

The IoT-based system is composed of a microcontroller with an ESP32 CAM module, MQ2 gas sensor and Neo 6M GPS module. The system periodically sends container data to the server, including a top-view image of the container and its location. The server has a pre-trained convolutional neural network (CNN) model which is used to analyze the image and determine the fullness level of the garbage container, in contrary to most past studies which have used depth sensors like ultrasonic sensors or weight sensors to determine the garbage fullness level. The server then sends the analyzed data to a web application, where the fullness data of the container is displayed on a map for monitoring purposes.

## IoT in the system

The system's hardware consists of the following components:

- Camera: Installed at the top of the garbage container, it takes pictures periodically. Used: AI thinker's ESP32 CAM module
- GPS: To locate the container to show it in the web application. Used: Neo6M GPS module

## CNN model

The Jupyter notebook with detailed description for training the model is included under filename **_Fullness determination with CNN.ipynb_** or [Click here](Fullness%20determination%20with%20CNN.ipynb)

## Data Collection and Model Improvement

One of the objectives of this project is to create a reliable and accurate dataset of images representing different levels of container fullness. Currently, the dataset contains only about a thousand images. Once deployed in the real world, the system will continue to store the images sent by the IoT device, along with their corresponding labels. To ensure reliability, only images confidently identified by the CNN model will be stored. This continual expansion of the dataset will eventually make the dataset more diverse, reliable, accurate, and valuable for future researchers. The dataset will be made publicly available, and will be provided free for use by interested parties.

## Navigating the repository

The code for programming the hardware is inside folder **_ESP32 CAM Sketch_**. There are two files
[**_for_creating_dataset_**](ESP32%20CAM%20Sketch/for_creating_dataset.ino) : program to take photos of container at different fullness levels
[**_garbage_monitor_final_**](ESP32%20CAM%20Sketch/for_creating_dataset.ino): the actual program used after hardware is deployed.

**_Server_** folder contains the code for the Flask server which serves requests from the IoT and the web application.

**_Web application for monitoring_** folder contains the React application.
