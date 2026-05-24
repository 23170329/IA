import cv2
import numpy as np
from typing import Generator, Tuple


class CaptureModule:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"No se pudo abrir el video: {video_path}")

        from moviepy import VideoFileClip
        clip = VideoFileClip(video_path)
        self.fps = clip.fps
        self.duration = clip.duration
        clip.close()

        if self.fps is None or self.fps <= 0:
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def extract_frames(self, sample_rate: float = 2.0) -> Generator[Tuple[np.ndarray, float], None, None]:
        step = max(1, int(self.fps / sample_rate))
        frame_idx = 0
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if frame_idx % step == 0:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                timestamp = frame_idx / self.fps
                yield frame_rgb, timestamp
            frame_idx += 1

    def get_total_samples(self, sample_rate: float = 2.0) -> int:
        step = max(1, int(self.fps / sample_rate))
        return self.total_frames // step

    def __del__(self):
        if hasattr(self, "cap") and self.cap.isOpened():
            self.cap.release()
