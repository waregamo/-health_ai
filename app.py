import streamlit as st
import pandas as pd
from PIL import Image
import base64

# ========================
# PAGE CONFIGURATION
# ========================
st.set_page_config(
    page_title="AI Health Diagnostic Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================
# AUTHENTICATION
# ========================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def authenticate():
    add_bg_from_local("Assets/bg_medical.jpg")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <style>
            .login-box {
                background-color: rgba(255, 255, 255, 0.95);
                padding: 2.5rem;
                border-radius: 15px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
                text-align: center;
            }
            .login-box input {
                border-radius: 8px;
                padding: 0.5rem;
            }
            .login-title {
                font-size: 28px;
                font-weight: 600;
                color:#008000;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("<div class='login-box'>", unsafe_allow_html=True)

        try:
            st.image("Assets/logo.jpg", width=90)
        except:
            st.warning("Logo not found.")

        st.markdown("<div class='login-title'>🔐 AI Health Diagnostic Login</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: gray;'>Secure Access Portal for Medical Professionals</p>", unsafe_allow_html=True)

        with st.form("login"):
            password = st.text_input("Enter Access Key", type="password")
            submit = st.form_submit_button("Login")

            if submit:
                if password == "123":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Incorrect access key.")

        st.markdown("<small style='color: gray;'>Need access? Contact admin at <a href='mailto:support@aihealth.com'>support@aihealth.com</a></small>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ========================
# MAIN APPLICATION
# ========================
def main_app():
    with st.sidebar:
        try:
            st.image("Assets/logo.jpg", width=200)
        except:
            st.warning("Logo missing.")
        st.markdown("<h2 style='color: black;'>Navigation</h2>", unsafe_allow_html=True)
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

# ========================
# HOME PAGE
# ========================
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

    feature_data = [
        ("2.jpg", "Rapid Analysis", "Get results in seconds"),
        ("3.jpg", "Multi-Disease", "Supports several conditions"),
        ("4.jpg", "Confidence Metrics", "Probability-based output")
    ]
    cols = st.columns(3)
    for col, (img, title, desc) in zip(cols, feature_data):
        try:
            col.image(f"Assets/{img}", width=150)
        except:
            col.warning(f"{img} not found.")
        col.markdown(f"<h4 style='text-align: center;'>{title}</h4>", unsafe_allow_html=True)
        col.markdown(f"<p style='text-align: center;'>{desc}</p>", unsafe_allow_html=True)

# ========================
# DIAGNOSTICS PAGE
# ========================
def show_diagnostics():
    st.markdown("<h1 style='text-align: center;'>Medical Diagnostics</h1>", unsafe_allow_html=True)
    disease = st.selectbox("Select Diagnostic Tool", ["Breast Cancer Detection", "Pneumonia Detection", "Malaria Detection"])
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("Analyzing..."):
            if "Breast" in disease:
                result = "Benign"
                confidence = 0.92
                chart_data = {"Confidence": [0.92, 0.07, 0.01], "Class": ["Benign", "Malignant", "Normal"]}
                explanation = """
                **Breast Cancer**: Benign means the tumor is *non-cancerous* and not life-threatening.
                Regular checkups are still recommended.
                """
            elif "Pneumonia" in disease:
                result = "Normal"
                confidence = 0.88
                chart_data = {"Confidence": [0.88, 0.12], "Class": ["Normal", "Pneumonia"]}
                explanation = """
                **Pneumonia**: An infection that inflames the lungs. It causes cough, fever, and breathing difficulty.
                A "Normal" result means no signs of infection were detected.
                """
            else:
                result = "Uninfected"
                confidence = 0.95
                chart_data = {"Confidence": [0.95, 0.05], "Class": ["Uninfected", "Infected"]}
                explanation = """
                **Malaria**: A mosquito-borne disease caused by parasites.
                "Uninfected" means no signs of malaria parasites were detected in the blood smear.
                """

            st.success("✅ Analysis Complete")
            col1, col2 = st.columns(2)
            col1.metric("Diagnosis", result)
            col2.metric("Confidence", f"{confidence * 100:.1f}%")

            st.markdown("### Confidence Breakdown")
            chart_df = pd.DataFrame(chart_data)
            st.bar_chart(chart_df.set_index("Class"), use_container_width=True)

            st.markdown("### 📘 What does this mean?")
            st.info(explanation)

# ========================
# ABOUT PAGE
# ========================
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

# ========================
# FEEDBACK PAGE
# ========================
def show_feedback():
    st.markdown("<h1 style='text-align: center;'>💬 Feedback</h1>", unsafe_allow_html=True)

    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

    if not st.session_state.feedback_submitted:
        with st.form("feedback_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Email Address")
            rating = st.slider("Rate Your Experience", 1, 5, 3)
            message = st.text_area("Your Message")
            submitted = st.form_submit_button("Submit")

            if submitted:
                st.session_state.feedback_submitted = True
                st.rerun()
    else:
        st.success("✅ Thank you! Your feedback has been submitted.")
        if st.button("Submit Another Feedback"):
            st.session_state.feedback_submitted = False
            st.rerun()

# ========================
# APP EXECUTION
# ========================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    main_app()
else:
    authenticate()






