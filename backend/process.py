import face_recognition
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.queries import *
from utils import *

def calculate_img_encodings(img_bytes):
    img_bgr = bytes_to_ndarray(img_bytes)
    print("imbgr: ", img_bgr)
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_encodings = face_recognition.face_encodings(img)

    if img_encodings:
        img_encodings = img_encodings[0]
        img_encodings = json.dumps(img_encodings.tolist())
        print("image Encoding: ", img_encodings)
        return img_encodings
    return ""


async def convert_img_to_bytes(img):
    file_bytes = await img.read()
    return file_bytes


def store_new_person(conn, first_name, last_name):
    person_id = insert_name(conn, first_name, last_name)
    print("New person is stored!")
    return person_id


def store_encodings(conn, person_id, img_encodings):
    encoding_id = insert_face_encoding(conn, person_id, img_encodings)
    print("New Encoding is stored!")
    return encoding_id


def store_img_bytes(conn, person_id, img_bytes):
    img_id = insert_image_bytes(conn, person_id, img_bytes)
    print("New image bytes is stored!")
    return img_id
