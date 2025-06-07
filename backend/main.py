from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import shutil
import os
from process import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
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
    # !!!!!!!!!!! needs to be implemented!


    return {"message": "Upload successful",
            "first name": firstName,
            "last name": lastName,
            "filename": imgUpload.filename}

@app.get("/api/feature")
async def feature():
    return {"feature-message": "This is a feature message"}