# Databricks notebook source

import tensorflow as tf
import base64

model_dir = 'models/openimages_v4_ssd_mobilenet_v2_1'
saved_model = tf.saved_model.load(model_dir)
detector = saved_model.signatures['default']


def predict(body):
    base64img = body.get('image')
    img_bytes = base64.decodebytes(base64img.encode())
    detections = detect(img_bytes)
    cleaned = clean_detections(detections)
    
    return { 'detections': cleaned }


def detect(img):    
    image = tf.image.decode_jpeg(img, channels=3)
    converted_img  = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
    result = detector(converted_img)
    num_detections = len(result["detection_scores"])
    
    output_dict = {key:value.numpy().tolist() for key, value in result.items()}
    output_dict['num_detections'] = num_detections
    
    return output_dict


def clean_detections(detections):
    cleaned = []
#     max_boxes = 10
#     num_detections = min(detections['num_detections'], max_boxes)
    num_detections = detections['num_detections']

    for i in range(0, num_detections):
        label = detections['detection_class_entities'][i].decode('utf-8')
        score = detections['detection_scores'][i]
        if label == 'Dog' and score > 0.3:
            d = {
                'box': {
                    'yMin': detections['detection_boxes'][i][0],
                    'xMin': detections['detection_boxes'][i][1],
                    'yMax': detections['detection_boxes'][i][2],
                    'xMax': detections['detection_boxes'][i][3]
                },
                'class': label,
                'label': label,
                'score': score,
            }
            cleaned.append(d)

    return cleaned
