# shared/utils/image_utils.py
import os
from PIL import Image  # Ensure Pillow library is added to your dependencies

def load_image(filename):
    resource_path = os.path.join(os.path.dirname(__file__), '../resources', filename)
    return Image.open(resource_path)

def capture_screenshot():
    # Implement the logic to capture a live screenshot
    return None
