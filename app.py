import gradio as gr
import pickle
import numpy as np
from report_processor import extract_numbers_from_report

# Models Load karein
model = pickle.load(open('diabetes_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

def predict_diabetes(preg, glucose, bp, skin, insulin, bmi, dpf, age):
    if any(x is None or x == 0 for x in [glucose, bmi, age]):
        return "⚠️ Error", "Please provide vital data (Glucose, BMI, Age)."

    features = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    prob = model.predict_proba(features_scaled)[0][1]
    
    if prediction[0] == 1:
        return f"🚨 HIGH RISK ({prob:.1%})", "Patient shows strong indicators of Diabetes. Immediate clinical consultation recommended."
    else:
        return f"✅ LOW RISK ({1-prob:.1%})", "Values are within normal range. Maintain healthy diet and regular exercise."

def handle_autofill(image):
    if image is None:
        return 0, 0, 0, 0, "No file uploaded."
    data, raw_text = extract_numbers_from_report(image)
    # Ensuring values are returned for the specific boxes
    return data.get('glucose', 0), data.get('bmi', 0), data.get('age', 0), data.get('bp', 0), raw_text

# --- UPDATED MODERN MEDICAL CSS ---
medical_style = """
.gradio-container { background: #f1f5f9; font-family: 'Inter', sans-serif; }
.main-header { text-align: center; color: #0f172a; padding: 25px; margin-bottom: 20px; }
.card { background: white; border-radius: 12px; padding: 20px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
.result-card { background: #f8fafc; border-radius: 12px; padding: 20px; border-left: 5px solid #2563eb; margin-top: 15px; }
.predict-btn { background: #2563eb !important; color: white !important; font-weight: bold !important; border-radius: 8px !important; }
.extract-btn { background: #f0fdf4 !important; color: #16a34a !important; border: 1px solid #16a34a !important; font-weight: bold !important; }
label { font-weight: 600 !important; margin-bottom: 5px; }
"""

with gr.Blocks(css=medical_style, theme=gr.themes.Soft(primary_hue="blue")) as demo:
    
    gr.HTML("""
        <div class="main-header">
            <h1 style='font-size: 2.2rem;'>🏥 HealthPredict AI</h1>
            <p style='color: #475569;'>Intelligent Diagnostic Support System for Medical Professionals</p>
        </div>
    """)
    
    with gr.Row():
        # LEFT: Manual Data Entry
        with gr.Column(scale=1):
            with gr.Group(elem_classes="card"):
                gr.Markdown("### 📋 Clinical Vitals")
                with gr.Row():
                    preg = gr.Number(label="Pregnancies", value=0)
                    age = gr.Number(label="Age (Years)", value=0)
                
                with gr.Row():
                    glucose = gr.Number(label="Glucose (mg/dL)", value=0)
                    bp = gr.Number(label="Blood Pressure (mmHg)", value=0)
                
                with gr.Row():
                    bmi = gr.Number(label="BMI Value", value=0)
                    dpf = gr.Number(label="Pedigree Function", value=0.47)
                
                with gr.Row():
                    skin = gr.Number(label="Skin Thickness", value=20)
                    insulin = gr.Number(label="Insulin Level", value=79)
                
                predict_btn = gr.Button("RUN ANALYSIS", elem_classes="predict-btn")

        # RIGHT: OCR & Results
        with gr.Column(scale=1):
            # Scanner Card
            with gr.Group(elem_classes="card"):
                gr.Markdown("### 📂 Report Scanner")
                report_file = gr.Image(type="filepath", label="Upload Medical Report")
                extract_btn = gr.Button("SCAN & AUTOFILL", elem_classes="extract-btn")
                with gr.Accordion("OCR Debug View", open=False):
                    raw_text = gr.Textbox(label="", lines=3)

            # Results Card
            with gr.Group(elem_classes="result-card"):
                gr.Markdown("### 📊 Diagnostic Output")
                result_display = gr.Label(label="Risk Assessment")
                advice_display = gr.Textbox(label="Clinical Recommendation", interactive=False)

    # Event Handlers
    extract_btn.click(
        fn=handle_autofill, 
        inputs=[report_file], 
        outputs=[glucose, bmi, age, bp, raw_text]
    )

    predict_btn.click(
        fn=predict_diabetes,
        inputs=[preg, glucose, bp, skin, insulin, bmi, dpf, age],
        outputs=[result_display, advice_display]
    )

    gr.Markdown("<p style='text-align: center; color: #94a3b8; padding-top: 20px;'>© 2026 HealthPredict AI System | Mid-Term Submission</p>")

demo.launch()
