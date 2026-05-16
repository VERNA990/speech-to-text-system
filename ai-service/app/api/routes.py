from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    filepath = f"{UPLOAD_DIR}/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Audio uploaded", "file": filepath}