import numpy as np
from PIL import Image
import torch


class VisionModule:
    MODEL_NAME = "Salesforce/blip-image-captioning-base"

    def __init__(self):
        print(f"[Vision] Cargando {self.MODEL_NAME}...")
        from transformers import BlipProcessor, BlipForConditionalGeneration
        self.processor = BlipProcessor.from_pretrained(self.MODEL_NAME)
        self.model = BlipForConditionalGeneration.from_pretrained(
            self.MODEL_NAME,
            torch_dtype=torch.float32,
        )
        self.model.eval()
        print("[Vision] BLIP listo")

    def caption_frame(self, frame_rgb: np.ndarray) -> str:
        image = Image.fromarray(frame_rgb)
        inputs = self.processor(image, return_tensors="pt")
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=60,
                num_beams=3,
            )
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption.strip()
