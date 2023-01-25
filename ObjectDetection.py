#!/usr/bin/env python

import sys
import cv2
import numpy as np
import os

def getObjects(path):
    # Loading Yolo
    net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    output_layers = net.getUnconnectedOutLayersNames()
    
    #Image Loading
    image = cv2.imread(path)
    image = cv2.resize(image, None, fx=0.4, fy=0.4)
    
    #Image Conversion and Network
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    #Detecting all the objects in the image with score > 50%
    class_ids = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence >= 0.5:
                class_ids.append(class_id)
    labels = []
    for i in range(len(class_ids)):
        labels.append(classes[class_ids[i]])
    return (labels)
