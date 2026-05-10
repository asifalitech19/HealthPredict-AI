import pytesseract
from PIL import Image
import re

# Tesseract Path (Apne PC ke mutabiq check karlein)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_numbers_from_report(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        extracted_data = {}
        
        # In patterns ko humne mazeed "loose" rakha hai taake noise handle ho sakay
        patterns = {
            "glucose": r"(?:Glucose|Sugar|GLU)[:\s]*(\d+)",
            "bmi": r"BMI[:\s]*(\d+\.?\d*)",
            "age": r"Age[:\s]*(\d+)",
            "bp": r"(?:BP|Blood Pressure|Pressure)[:\s]*(\d+)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_data[key] = float(match.group(1))
            else:
                extracted_data[key] = None # Autofill ke liye None rakhein taake purana data na chore
                
        return extracted_data, text
    except Exception as e:
        return {}, f"Error: {str(e)}"
        