import numpy as np
import cv2


class HeuristicModule:
    def __init__(self, threshold: float = 150.0, min_interval: float = 2.5):
        self.threshold = threshold
        self.min_interval = min_interval
        self.prev_frame_gray = None
        self.last_comment_time = -999.0
        self.recent_changes = []
        self._has_changed = False
        self._commented_events: set[str] = set()

        self.game_over_detected = False
        self.is_board_full = False
        self.fill_percentage = 0.0
        self._prev_fill_percentage = 0.0
        self.last_mse = 0.0
        self.full_and_static_count = 0

    def _mse(self, frame1_gray: np.ndarray, frame2_gray: np.ndarray) -> float:
        diff = frame1_gray.astype(float) - frame2_gray.astype(float)
        return float(np.mean(diff ** 2))

    def get_pacing(self, timestamp: float) -> str:
        recent = [t for t in self.recent_changes if timestamp - t < 5]
        return "nervioso" if len(recent) >= 3 else "normal"

    def _compute_fill_percentage(self, frame_rgb: np.ndarray) -> float:
        gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
        height, width = gray.shape

        y_top = int(height * 0.12)
        y_bottom = int(height * 0.85)
        x_start = int(width * 0.38)
        x_end = int(width * 0.62)

        board = gray[y_top:y_bottom, x_start:x_end]
        if board.size == 0:
            return 0.0

        h, w = board.shape

        col_heights = []
        step = max(1, w // 15)

        for col in range(0, w, step):
            col_data = board[:, col]
            bright = col_data > 50

            bright_indices = np.where(bright)[0]
            if len(bright_indices) == 0:
                continue

            bottom_bright = bright_indices[-1]

            if bottom_bright < h // 2:
                continue

            GAP_TOLERANCE = 2
            highest_in_stack = bottom_bright
            consecutive_dark = 0

            for j in range(bottom_bright - 1, -1, -1):
                if bright[j]:
                    highest_in_stack = j
                    consecutive_dark = 0
                else:
                    consecutive_dark += 1
                    if consecutive_dark > GAP_TOLERANCE:
                        break

            col_heights.append(highest_in_stack)

        if not col_heights:
            return 0.0

        median_h = float(np.median(col_heights))
        fill_pct = 1.0 - (median_h / h)
        return float(max(0.0, min(fill_pct, 1.0)))

    def has_commented(self, event: str) -> bool:
        return event in self._commented_events

    def mark_commented(self, event: str):
        self._commented_events.add(event)

    def feed_frame(self, frame_rgb: np.ndarray, timestamp: float):
        height, width, _ = frame_rgb.shape
        x_start = int(width * 0.38)
        x_end = int(width * 0.62)
        y_start = int(height * 0.12)
        y_end = int(height * 0.85)

        board_crop = frame_rgb[y_start:y_end, x_start:x_end]
        if board_crop.size > 0:
            gray = cv2.cvtColor(board_crop, cv2.COLOR_RGB2GRAY)
            gray_small = cv2.resize(gray, (80, 160))
        else:
            gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
            gray_small = cv2.resize(gray, (160, 90))

        self._has_changed = False
        self.last_mse = 0.0

        if self.prev_frame_gray is not None:
            mse_val = self._mse(self.prev_frame_gray, gray_small)
            self.last_mse = mse_val
            if mse_val >= self.threshold:
                self.recent_changes.append(timestamp)
                self.recent_changes = [t for t in self.recent_changes if timestamp - t < 10]
                self._has_changed = True
                self.prev_frame_gray = gray_small
        else:
            self.prev_frame_gray = gray_small
            self._has_changed = True

    def analyze_board_state(self, frame_rgb: np.ndarray, timestamp: float):
        if timestamp < 2.0:
            return

        self._prev_fill_percentage = self.fill_percentage
        self.fill_percentage = self._compute_fill_percentage(frame_rgb)

        self.is_board_full = self.fill_percentage >= 0.75

        if self.game_over_detected:
            return

        height, width, _ = frame_rgb.shape
        gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
        hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)

        if self.fill_percentage >= 0.99:
            self.game_over_detected = True
            return

        y_board_end = int(height * 0.85)
        y_top_start = int(height * 0.12)
        x_start = int(width * 0.38)
        x_end = int(width * 0.62)

        board_gray = gray[y_top_start:y_board_end, x_start:x_end]
        board_hsv = hsv[y_top_start:y_board_end, x_start:x_end]

        board_blocks_mask = board_gray > 50
        num_block_pixels = np.sum(board_blocks_mask)

        if num_block_pixels > (board_gray.size * 0.05) and self.fill_percentage > 0.6:
            block_saturation = board_hsv[:, :, 1][board_blocks_mask]
            avg_saturation = np.mean(block_saturation)
            if avg_saturation < 25:
                self.game_over_detected = True
                return

        if self.fill_percentage >= 0.95 and self.last_mse < 30.0:
            self.full_and_static_count += 1
            if self.full_and_static_count >= 5:
                self.game_over_detected = True
                return
        else:
            self.full_and_static_count = max(0, self.full_and_static_count - 1)

        board_mean = np.mean(board_gray)
        if board_mean < 30 and self._prev_fill_percentage >= 0.9 and self.fill_percentage < 0.3:
            self.game_over_detected = True

    def should_comment(self, timestamp: float, force: bool = False) -> bool:
        if force:
            self.last_comment_time = timestamp
            return True
        time_ok = (timestamp - self.last_comment_time) >= self.min_interval
        return self._has_changed and time_ok

    def reset(self):
        self.prev_frame_gray = None
        self.last_comment_time = -999.0
        self.recent_changes = []
        self._has_changed = False
        self._commented_events.clear()
        self.game_over_detected = False
        self.is_board_full = False
        self.fill_percentage = 0.0
        self._prev_fill_percentage = 0.0
        self.last_mse = 0.0
        self.full_and_static_count = 0
