import torch
import torch.nn as nn
import open_clip


class ImageEncoder(nn.Module):
    def __init__(self):
        super().__init__()

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained="openai"
        )

        self.output_dim = 512

    def forward(self, images):
        features = self.model.encode_image(images)
        return features