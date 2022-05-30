import cv2


def resize_max(src, size_max: int):
    """
    Resize image to size_max (width or height) with save ratio

    Parameters:
        src (image): OpenCV image object
        size_max (int): Maximum size along width or height

    Returns:
        Scaled image
    """
    h, w = src.shape[:2]
    max_hw = max(h, w)
    return cv2.resize(src, (int(w / max_hw * size_max), int(h / max_hw * size_max)))
