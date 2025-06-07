import numpy as np
import cv2

def bytes_to_ndarray(img_bytes: bytes) -> np.ndarray:
    # Convert bytes to 1D numpy array
    nparr = np.frombuffer(img_bytes, np.uint8)
    # Decode image array from buffer
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR format
    return img