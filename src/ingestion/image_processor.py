from PIL import Image
import pytesseract
import os
from typing import Dict, Any

class ImageProcessor:
    def __init__(self):
        # Verify pytesseract is installed and reachable
        pass

    def process_image(self, file_path: str) -> Dict[str, Any]:
        """
        Processes a standalone image (JPG/PNG) to extract text via OCR.
        """
        print(f"Processing Image: {file_path}...")
        
        try:
            image = Image.open(file_path)
            
            # Perform OCR to get text from the image
            extracted_text = pytesseract.image_to_string(image)
            
            return {
                "type": "image",
                "content": extracted_text, # The text found in the image
                "image_path": file_path,   # The path to the actual image file
                "metadata": {
                    "source": file_path,
                    "filename": os.path.basename(file_path),
                    "page_number": 1 # Standalone images are always page 1
                }
            }
        except Exception as e:
            print(f"Error processing image {file_path}: {e}")
            return None

if __name__ == "__main__":
    processor = ImageProcessor()
    # processor.process_image("sample_documents/test_image.png")