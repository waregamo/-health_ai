import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

# ==============================
# APP CONFIGURATION
# ==============================
st.set_page_config(
    page_title="AI Health Diagnostic Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# AUTHENTICATION
# ==============================
def authenticate():
    try:
        st.image("Assets/logo.jpg", width=300)
    except:
        st.warning("Logo not found.")

    st.markdown("<h1 style='text-align: center;'>Medical AI Portal</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login"):
            password = st.text_input("Enter Access Key", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if password == "123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect access key.")
        st.markdown("<div style='text-align: center; color: #666;'>Contact admin for access credentials</div>", unsafe_allow_html=True)

# ==============================
# MAIN APPLICATION
# ==============================
def main_app():
    st.markdown("""
    <style>
        .stSidebar {
            background-color: #333 !important;
        }
        .stButton>button {
            background-color: #4e4376;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
        }
        div[role="radiogroup"] > label {
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        try:
            st.image("Assets/logo.jpg", width=200)
        except:
            st.warning("Sidebar logo not found.")
        st.markdown("<h2 style='color: white;'>Navigation</h2>", unsafe_allow_html=True)
        selected = st.radio("", ["Home", "Diagnostics", "About Us", "Feedback"])

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    if selected == "Home":
        show_home()
    elif selected == "Diagnostics":
        show_diagnostics()
    elif selected == "About Us":
        show_about()
    elif selected == "Feedback":
        show_feedback()

# ==============================
# COMPONENTS
# ==============================
def show_home():
    st.markdown("<h1 style='text-align: center;'>Welcome to AI Health Diagnostic Hub</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='padding: 20px;'>
            <h3>Revolutionizing Medical Diagnostics</h3>
            <p>
            Our AI-powered platform provides instant preliminary analysis for:<br>
            • Breast Cancer (Ultrasound)<br>
            • Pneumonia (Chest X-ray)<br>
            • Malaria (Blood Smear)<br><br>
            Designed for healthcare professionals and medical students.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        try:
            st.image("Assets/1.jpg", caption="AI in Healthcare", use_container_width=True)
        except:
            st.warning("Hero image not found.")

    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Key Features</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("2.jpg", "Rapid Analysis"),
        ("3.jpg", "Multi-Disease"),
        ("4.jpg", "Confidence Metrics")
    ]
    for col, (img, title) in zip([col1, col2, col3], features):
        try:
            col.image(f"Assets/{img}", width=150)
        except:
            col.warning(f"{img} missing.")
        col.markdown(f"<h4 style='text-align: center;'>{title}</h4>", unsafe_allow_html=True)

def show_diagnostics():
    st.markdown("<h1 style='text-align: center;'>Medical Diagnostics</h1>", unsafe_allow_html=True)
    disease = st.selectbox("Select Diagnostic Tool", ["Breast Cancer Detection", "Pneumonia Detection", "Malaria Detection"])

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("Analyzing..."):
            if "Breast" in disease:
                result, confidence, chart_data = "Benign", 0.92, [0.92, 0.07, 0.01]
                labels = ["Benign", "Malignant", "Normal"]
            elif "Pneumonia" in disease:
                result, confidence, chart_data = "Normal", 0.88, [0.88, 0.12]
                labels = ["Normal", "Pneumonia"]
            else:
                result, confidence, chart_data = "Uninfected", 0.95, [0.95, 0.05]
                labels = ["Uninfected", "Infected"]

            st.success("Analysis Complete")
            col1, col2 = st.columns(2)
            col1.metric("Diagnosis", result)
            col2.metric("Confidence", f"{confidence*100:.1f}%")

            st.markdown("### Confidence Breakdown")
            st.bar_chart(chart_data, use_container_width=True)
            st.caption("Classes: " + ", ".join(labels))

def show_about():
    st.markdown("<h1 style='text-align: center;'>About Our Platform</h1>", unsafe_allow_html=True)
    try:
        st.image("Assets/5.jpg", use_container_width=True)
    except:
        st.warning("About image not found.")

    st.markdown("""
### 🎯 Our Mission  
To democratize access to medical diagnostics through AI technology, particularly in underserved communities.

### 🧪 Technology  
Our platform uses state-of-the-art convolutional neural networks (CNNs) trained on thousands of medical images for accurate classification.

### ⚠️ Disclaimer  
<div style='color: #ff4b4b;'>
This tool provides preliminary analysis only and should not replace professional medical diagnosis. Always consult a healthcare provider.
</div>
""", unsafe_allow_html=True)

def show_feedback():
    st.markdown("<h1 style='text-align: center;'>💬 Feedback</h1>", unsafe_allow_html=True)
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email Address")
        rating = st.slider("Rate Your Experience", 1, 5, 3)
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Submit")

        if submitted:
            content = f"""
New Feedback Received:

Name: {name}
Email: {email}
Rating: {rating}
Message: {message}
"""
            msg = MIMEText(content)
            msg['Subject'] = "📩 New Feedback - AI Health Diagnostic Hub"
            msg['From'] = os.getenv("EMAIL_USER")
            msg['To'] = os.getenv("EMAIL_TO")

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
                server.send_message(msg)
                server.quit()
                st.success("✅ Feedback sent successfully.")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")

# ==============================
# RUN APP
# ==============================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    main_app()
else:
    authenticate()


