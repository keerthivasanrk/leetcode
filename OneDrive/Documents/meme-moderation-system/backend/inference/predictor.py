import torch
from PIL import Image
from torchvision import transforms

from backend.models.text_model import TextEncoder
from backend.models.vision import ImageEncoder
from backend.models.fusion_model import FusionModel
from backend.ocr.ocr_engine import extract_text

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
THRESHOLD = 0.5


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


text_encoder = TextEncoder().to(DEVICE)
vision_encoder = ImageEncoder().to(DEVICE)

fusion_model = FusionModel().to(DEVICE)
fusion_model.load_state_dict(torch.load("weights/fusion_model.pt", map_location=DEVICE))
fusion_model.eval()


def predict(image_path: str):
    with torch.no_grad():

        # ---- OCR ----
        extracted_text = extract_text(image_path)

        # ---- Image ----
        image = Image.open(image_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

        # ---- Encoders ----
        img_feat = vision_encoder(image_tensor)
        txt_feat = text_encoder([extracted_text])

        # ---- Fusion ----
        logits = fusion_model(img_feat, txt_feat)
        score = torch.sigmoid(logits).item()

        label = "HATEFUL" if score >= THRESHOLD else "SAFE"

        return {
            "classification": label,
            "confidence": round(score, 4),
            "extracted_text": extracted_text
        }