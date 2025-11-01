import base64
import os
from django.conf import settings

def get_logo_base64():
    """Convert the logo image to base64 string for email embedding"""
    logo_path = os.path.join(settings.STATIC_ROOT, 'logo', 'Gemini_Generated_Image_rxlcwrxlcwrxlcwr.png')
    try:
        with open(logo_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading logo file: {e}")
        return None