import cv2


def resize_max(src, size_max):
    h, w = src.shape[:2]
    max_hw = max(h, w)
    return cv2.resize(src, (int(w / max_hw * size_max), int(h / max_hw * size_max)))
