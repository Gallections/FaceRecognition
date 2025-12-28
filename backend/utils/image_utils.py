"""
Utility functions for backend
"""
import numpy as np
import cv2


def bytes_to_ndarray(img_bytes: bytes) -> np.ndarray:
    """
    Convert image bytes to numpy array
    
    Args:
        img_bytes: Image data as bytes
        
    Returns:
        Numpy array in BGR format
    """
    # Convert bytes to 1D numpy array
    nparr = np.frombuffer(img_bytes, np.uint8)
    # Decode image array from buffer
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR format
    return img


def ndarray_to_bytes(img: np.ndarray, format: str = '.jpg') -> bytes:
    """
    Convert numpy array to image bytes
    
    Args:
        img: Image as numpy array
        format: Image format (default: .jpg)
        
    Returns:
        Image data as bytes
    """
    success, buffer = cv2.imencode(format, img)
    if not success:
        raise ValueError("Failed to encode image")
    return buffer.tobytes()
