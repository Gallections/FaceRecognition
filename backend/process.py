import numpy as np
import face_recognition_models
import face_recognition
import cv2
import json
import os
from datetime import datetime

from database.queries import *
from utils import *

def calculate_img_encodings(img_bytes):
    img_bgr = bytes_to_ndarray(img_bytes)
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_encodings = face_recognition.face_encodings(img)

    if img_encodings:
        img_encodings = img_encodings[0]
        img_encodings = json.dumps(img_encodings.tolist())
        return img_encodings
    return ""


async def convert_img_to_bytes(img):
    file_bytes = await img.read()
    return file_bytes


def store_new_person(first_name, last_name):
    person_id = insert_name(first_name, last_name);
    return person_id


def store_encodings(person_id, img_encodings):
    encoding_id = insert_face_encoding(person_id, img_encodings)
    return encoding_id


def store_img_bytes(person_id, img_bytes):
    img_id = insert_image_bytes(person_id, img_bytes);
    return img_id

# def master_store(firstname, lastname):
#     person_id = store_new_person(firstname, lastname)
#     calculate_img_encodings()
