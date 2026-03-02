import os
import pandas as pd
from tqdm import tqdm
from backend.ocr.ocr_engine import extract_text

IMAGE_DIR = "backend/datasets/TRAINING"
ORIGINAL_CSV = "backend/datasets/TRAINING/train.csv"
OUTPUT_CSV = "backend/datasets/TRAINING/train_ocr.csv"

def main():
    df = pd.read_csv(ORIGINAL_CSV)
    ocr_texts = []

    print("Running OCR on training images...")

    for _, row in tqdm(df.iterrows(), total=len(df)):
        img_path = os.path.join(IMAGE_DIR, row["file_name"])
        text = extract_text(img_path)
        ocr_texts.append(text)

    df["text"] = ocr_texts
    df.to_csv(OUTPUT_CSV, index=False)

    print("OCR training dataset saved as train_ocr.csv")

if __name__ == "__main__":
    main()
