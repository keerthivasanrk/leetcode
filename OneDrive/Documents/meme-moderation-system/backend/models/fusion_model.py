import torch
import torch.nn as nn


class FusionModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc = nn.Sequential(
            nn.Linear(512 + 768, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )

    def forward(self, img_feat, txt_feat):
        fused = torch.cat([img_feat, txt_feat], dim=1)
        return self.fc(fused)