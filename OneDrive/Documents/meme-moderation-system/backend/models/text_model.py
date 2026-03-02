import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel


class TextEncoder(nn.Module):
    def __init__(self):
        super().__init__()

        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")

        self.output_dim = 768

    def forward(self, texts):
        tokens = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )

        tokens = {k: v.to(next(self.model.parameters()).device)
                  for k, v in tokens.items()}

        outputs = self.model(**tokens)

        pooled = outputs.last_hidden_state[:, 0, :]
        return pooled