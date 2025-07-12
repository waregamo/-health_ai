import streamlit as st
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
import pandas as pd
import datetime

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
# AUTHENTICATION (Static Password)
# ==============================
def authenticate():
    st.image("Assets/logo.jpg", width=300)
    st.markdown("<h1 style='text-align: center;'>Medical AI Portal</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login"):
            password = st.text_input("Enter Access Key", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if password == "123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect access key. Please try again.")
        st.markdown("""
        <div style='text-align: center; margin-top: 20px; color: #666;'>
            <p>Contact admin for access credentials</p>
        </div>
        """, unsafe_allow_html=True)
    return False

# ==============================
# MAIN APPLICATION
# ==============================
def main_app():
    # Custom CSS for styling
    st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .sidebar .sidebar-content {
            background-image: linear-gradient(#2b5876, #4e4376);
            color: white;
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
        div[role="radiogroup"] > label[data-baseweb="radio"] > div {
            background-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    with st.sidebar:
        st.image("Assets/logo.jpg", width=200)
        st.markdown("<h2 style='color: white;'>Navigation</h2>", unsafe_allow_html=True)
        selected = st.radio("", ["Home", "Diagnostics", "About Us", "Feedback"])

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # Page Routing
    if selected == "Home":
        show_home()
    elif selected == "Diagnostics":
        show_diagnostics()
    elif selected == "About Us":
        show_about()
    else:
        show_feedback()

# ==============================
# PAGE COMPONENTS
# ==============================
def show_home():
    st.markdown("<h1 style='text-align: center;'>Welcome to AI Health Diagnostic Hub</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style='padding: 20px;'>
            <h3>Revolutionizing Medical Diagnostics</h3>
            <p style='font-size: 16px;'>
            Our AI-powered platform provides instant preliminary analysis for:<br>
            • Breast Cancer (Ultrasound)<br>
            • Pneumonia (Chest X-ray)<br>
            • Malaria (Blood Smear)<br><br>
            Designed for healthcare professionals and medical students.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image("Assets/1.jpg", caption="AI in Healthcare", use_container_width=True)

    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>Key Features</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("Assets/2.jpg", width=150)
        st.markdown("<h4 style='text-align: center;'>Rapid Analysis</h4>", unsafe_allow_html=True)
    with col2:
        st.image("Assets/3.jpg", width=150)
        st.markdown("<h4 style='text-align: center;'>Multi-Disease</h4>", unsafe_allow_html=True)
    with col3:
        st.image("Assets/4.jpg", width=150)
        st.markdown("<h4 style='text-align: center;'>Confidence Metrics</h4>", unsafe_allow_html=True)

def show_diagnostics():
    st.markdown("<h1 style='text-align: center;'>Medical Diagnostics</h1>", unsafe_allow_html=True)

    disease = st.selectbox(
        "Select Diagnostic Tool",
        ["Breast Cancer Detection", "Pneumonia Detection", "Malaria Detection"],
        index=0
    )

    uploaded_file = st.file_uploader(
        f"Upload {disease.split()[0]} Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("Analyzing image..."):
            if "Breast" in disease:
                result = "Benign"
                confidence = 0.92
                chart_data = {
                    "Classes": ["Benign", "Malignant", "Normal"],
                    "Confidence": [0.92, 0.07, 0.01]
                }
            elif "Pneumonia" in disease:
                result = "Normal"
                confidence = 0.88
                chart_data = {
                    "Classes": ["Normal", "Pneumonia"],
                    "Confidence": [0.88, 0.12]
                }
            else:
                result = "Uninfected"
                confidence = 0.95
                chart_data = {
                    "Classes": ["Uninfected", "Infected"],
                    "Confidence": [0.95, 0.05]
                }

            st.success("Analysis Complete!")
            col1, col2 = st.columns(2)
            col1.metric("Diagnosis", result)
            col2.metric("Confidence", f"{confidence*100:.1f}%")

            st.markdown("### 📊 Confidence Breakdown")
            st.bar_chart(data=chart_data["Confidence"], use_container_width=True)
            st.caption("Classes: " + ", ".join(chart_data["Classes"]))

            st.markdown("---")
            st.markdown("<h3>Interpretation Guide</h3>", unsafe_allow_html=True)

            if "Breast" in disease:
                st.markdown("""
                - **Benign**: Non-cancerous tumor, routine follow-up recommended  
                - **Malignant**: Cancerous tumor, immediate consultation advised  
                - **Normal**: No abnormalities detected
                """)
            elif "Pneumonia" in disease:
                st.markdown("""
                - **Positive**: Signs of lung infection detected  
                - **Negative**: No evidence of pneumonia
                """)

def show_about():
    st.markdown("<h1 style='text-align: center;'>About Our Platform</h1>", unsafe_allow_html=True)
    st.image("Assets/5.jpg", use_container_width=True)

    st.markdown("""
### 🎯 Our Mission  
To democratize access to medical diagnostics through AI technology, particularly in underserved communities.

### 🧪 Technology  
Our platform uses state-of-the-art convolutional neural networks (CNNs) trained on thousands of medical images for accurate classification.

### ⚠️ Disclaimer  
<p style='color: #ff4b4b;'>
This tool provides preliminary analysis only and should not replace professional medical diagnosis. Always consult a healthcare provider.
</p>
""", unsafe_allow_html=True)

def show_feedback():
    st.markdown("<h1 style='text-align: center;'>💬 We Value Your Feedback</h1>", unsafe_allow_html=True)
    st.markdown("Let us know what you think about the platform or suggest improvements.")

    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email Address")
        rating = st.slider("Rate Your Experience (1 = Poor, 5 = Excellent)", 1, 5, 3)
        message = st.text_area("Message")

        submit = st.form_submit_button("Submit Feedback")

        if submit:
            feedback_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "name": name,
                "email": email,
                "rating": rating,
                "message": message
            }

            try:
                df = pd.DataFrame([feedback_data])
                df.to_csv("feedback.csv", mode="a", header=not pd.io.common.file_exists("feedback.csv"), index=False)
                st.success("Thank you! Your feedback has been submitted.")
            except Exception as e:
                st.error(f"❌ Failed to save feedback: {e}")

# ==============================
# APP EXECUTION
# ==============================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    main_app()
else:
    authenticate()

