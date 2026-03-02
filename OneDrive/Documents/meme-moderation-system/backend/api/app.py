from fastapi import FastAPI, UploadFile, File
import shutil
import os

from backend.inference.predictor import predict

app = FastAPI()

UPLOAD_DIR = "backend/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/predict")
async def predict_meme(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict(file_path)

    return result