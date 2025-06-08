from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import shutil
import os
from process import *
from database.db import get_connection, close_connection

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

conn = get_connection()

app = FastAPI()

origins = [
    "http://localhost:5173",  # frontend origin
    # you can add more origins here if needed
    "http://localhost:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins =origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

USER_UPLOAD_DIR = "./uploads"
os.makedirs(USER_UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/uploads/images")
async def upload_image(
        imgUpload: Annotated[UploadFile, File()],
        firstName: str = Form("no description"),
        lastName: str = Form("no description")):

    img_bytes = await imgUpload.read()
    img_encodings = calculate_img_encodings(img_bytes)

    if img_encodings == "":
        return {"message": "Upload Invalid: No face is detected"}

    file_location = os.path.join(USER_UPLOAD_DIR, imgUpload.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(imgUpload.file, buffer)

    # Store all the information to database
    person_id = store_new_person(conn, firstName, lastName)
    store_encodings(conn, person_id, img_encodings)
    store_img_bytes(conn, person_id, img_bytes)

    return {"message": "Upload successful",
            "first name": firstName,
            "last name": lastName,
            "filename": imgUpload.filename}

@app.get("/api/feature")
async def feature():
    return {"feature-message": "This is a feature message"}