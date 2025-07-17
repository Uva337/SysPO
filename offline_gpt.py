"""offline_gpt.py
Local GPT-Neo assistant for offline inference.
"""
from __future__ import annotations

import os
from typing import Optional

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class LocalGPTAssistant:
    """Simple wrapper around GPT-Neo 125M for offline usage."""

    def __init__(self, model_dir: str = "models/gpt-neo-125M"):
        # Allow overriding the model path via environment variable
        env_dir = os.environ.get("GPT_NEO_PATH")
        self.model_dir = env_dir or model_dir
        self.model: Optional[torch.nn.Module] = None
        self.tokenizer: Optional[AutoTokenizer] = None

    def load_model(self) -> None:
        """Load model and tokenizer from ``self.model_dir``."""
        if self.model is not None:
            return
        if not os.path.isdir(self.model_dir):
            msg = (
                f"Model directory '{self.model_dir}' not found. "
                "Place the HF model there or set GPT_NEO_PATH environment variable."
            )
            raise FileNotFoundError(msg)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_dir)
        self.model.eval()

    def generate(self, prompt: str, max_length: int = 128) -> str:
        """Generate response for ``prompt``."""
        if self.model is None or self.tokenizer is None:
            self.load_model()
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            output = self.model.generate(**inputs, max_length=max_length)
        text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return text[len(prompt):].strip()

