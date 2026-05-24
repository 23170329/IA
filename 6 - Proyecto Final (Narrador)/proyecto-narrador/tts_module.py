import numpy as np
import torch
from typing import Tuple

_PAD_START = 0.25
_PAD_END = 0.55


class TTSModule:
    MODEL_NAME = "facebook/mms-tts-spa"

    def __init__(self):
        print(f"[TTS] Cargando {self.MODEL_NAME}...")
        from transformers import VitsModel, AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = VitsModel.from_pretrained(self.MODEL_NAME)
        self.model.eval()
        self.sample_rate = self.model.config.sampling_rate
        self._cache: dict[str, Tuple[int, np.ndarray]] = {}
        print(f"[TTS] MMS-TTS-SPA listo (sample rate: {self.sample_rate} Hz)")

    def synthesize(self, text: str) -> Tuple[int, np.ndarray]:
        if not text or not text.strip():
            silence = np.zeros(self.sample_rate, dtype=np.float32)
            return self.sample_rate, silence

        text = text.strip()
        if text in self._cache:
            return self._cache[text]

        if text[-1] not in ".!?":
            text += "."

        inputs = self.tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            output = self.model(**inputs).waveform

        waveform = output.squeeze().cpu().numpy().astype(np.float32)

        peak = np.abs(waveform).max()
        if peak > 0:
            waveform = waveform / peak * 0.88

        fade_in_samples = int(self.sample_rate * 0.02)
        if len(waveform) > fade_in_samples:
            fade_in = np.linspace(0.0, 1.0, fade_in_samples)
            waveform[:fade_in_samples] *= fade_in

        fade_out_samples = int(self.sample_rate * 0.06)
        if len(waveform) > fade_out_samples:
            fade_out = np.linspace(1.0, 0.0, fade_out_samples)
            waveform[-fade_out_samples:] *= fade_out

        pad_start = np.zeros(int(self.sample_rate * _PAD_START), dtype=np.float32)
        pad_end = np.zeros(int(self.sample_rate * _PAD_END), dtype=np.float32)

        waveform = np.concatenate([pad_start, waveform, pad_end])

        result = (self.sample_rate, waveform)
        self._cache[text] = result
        return result
