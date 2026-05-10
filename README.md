# 🏥 HealthPredict AI: Smart Health Advisor

HealthPredict AI is an intelligent diagnostic support tool developed for the **BS AI 6thsemester OpenEnded Lab**.It bridges the gap between clinical lab reports and automated health screening. 

## 🌟 Key Features
**OCR Scanning:** Utilizing Tesseract OCR to extract Glucose, BMI, and Age from medical reports. 
**Predictive AI:** Highaccuracy risk assessment using a **Random Forest Classifier**. 
**Smart Autofill:** Automatically populates GUI fields from parsed report data. 
**Medical Dashboard:** Userfriendly interface built with Gradio and custom CSS. 

## 🛠️ Technical Stack
**Machine Learning:** Scikitlearn, NumPy, Pandas 
**Computer Vision:** Pytesseract (OCR Engine) [cite: 11]
**Frontend:** Gradio 

## 📂 Project Modules
*`app.py`: Handles the UI and diagnostic logic. 
*`report_processor.py`: Manages image processing and Regexbased extraction. 
*`train_model.py`: Script used to train and serialize the model. 

## 🚀 Setup & Installation
1. Install **Tesseract OCR** on your local system.
2. Clone this repository.
3. Install dependencies: `pip install r requirements.txt`.
4. Run: `python app.py`.


*Developed by Asif Ali | Karachi, Pakistan*
