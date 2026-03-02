import os
import torch
import torch.nn as nn
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from tqdm import tqdm
from torchvision import transforms

from backend.models.text_model import TextEncoder
from backend.models.vision import ImageEncoder
from backend.models.fusion_model import FusionModel
print("TRAIN SCRIPT UPDATED VERSION LOADED")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CSV_PATH = "backend/datasets/TRAINING/train_ocr.csv"
IMAGE_DIR = "backend/datasets/TRAINING"



image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


class MemeDataset(Dataset):
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        img_path = os.path.join(IMAGE_DIR, row["file_name"])

        image = Image.open(img_path).convert("RGB")
        image = image_transform(image)   # ✅ now tensor

        text = str(row["text"])
        label = torch.tensor(row["label"], dtype=torch.float32)

        return image, text, label


def main():

    print("USING CSV:", CSV_PATH)

    image_encoder = ImageEncoder().to(DEVICE)
    text_encoder = TextEncoder().to(DEVICE)
    fusion_model = FusionModel().to(DEVICE)

    dataset = MemeDataset(CSV_PATH)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(fusion_model.parameters(), lr=1e-4)

    EPOCHS = 8

    for epoch in range(EPOCHS):

        fusion_model.train()
        total_loss = 0

        print(f"\n===== EPOCH {epoch+1}/{EPOCHS} =====")

        for batch_idx, (images, texts, labels) in enumerate(tqdm(loader)):

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            img_feat = image_encoder(images)
            txt_feat = text_encoder(list(texts))

            logits = fusion_model(img_feat, txt_feat)

            loss = criterion(logits.squeeze(), labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            if batch_idx % 50 == 0:
                print(f"Batch {batch_idx}/{len(loader)} | Loss: {loss.item():.4f}")

        print("Epoch Loss:", total_loss / len(loader))

    torch.save(fusion_model.state_dict(), "fusion_model.pt")
    print("Training finished. Model saved.")


if __name__ == "__main__": 
    main()
