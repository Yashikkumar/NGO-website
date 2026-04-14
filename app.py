import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Ektamission NGO", page_icon="🕊️", layout="centered")

# --- 2. INJECT CUSTOM HTML/CSS ---
# This hides the default Streamlit styling and applies your exact HTML styling
st.markdown("""
    <style>
    /* Hide Streamlit Header and Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    /* Apply Font to the whole app */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Custom Hero Section CSS */
    .hero {
        background: linear-gradient(to right, orange, black);
        color: white;
        padding: 80px 20px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .hero h2 {
        font-size: 40px;
        color: white !important;
        margin-bottom: 0px;
        font-weight: 600;
    }
    
    /* Custom Card CSS */
    .custom-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #eee;
    }
    .custom-card h3 {
        color: orange;
    }
    
    /* Style the Streamlit Form Button to match yours */
    div.stButton > button:first-child {
        background-color: orange;
        color: black;
        border: none;
        padding: 10px 30px;
        font-size: 18px;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: darkorange;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def init_google_sheets():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        if "gcp_credentials_json" in st.secrets:
            creds_dict = json.loads(st.secrets["gcp_credentials_json"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        return client.open('EktaMission_Contacts').sheet1
    except Exception as e:
        st.error(f"Could not connect to Google Sheets: {e}")
        return None

sheet = init_google_sheets()

# --- 4. HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("logo.png", width=80)
with col2:
    st.markdown("<h1 style='color: orange; margin:0; padding:0;'>Ektamission</h1>", unsafe_allow_html=True)

# --- 5. HERO SECTION (Using exact HTML) ---
st.markdown("""
<div class="hero">
  <h2>Together for Humanity</h2>
  <p style="font-size: 18px;">Unity beyond all religions — Ekta Mission</p>
</div>
""", unsafe_allow_html=True)

# --- 6. ABOUT US ---
st.markdown("<h2 style='text-align: center;'>About Us</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ektamission is a non-profit organization working for unity, peace, and social welfare. We believe in helping humanity beyond caste, religion, and boundaries.</p>", unsafe_allow_html=True)

st.write("---")

# --- 7. OUR WORK (Using exact HTML Cards) ---
st.markdown("<h2 style='text-align: center;'>Our Work</h2>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; gap: 20px; justify-content: center;">
    <div class="custom-card" style="flex: 1;">
      <h3>Food Distribution</h3>
      <p>Providing meals to the needy.</p>
    </div>
    <div class="custom-card" style="flex: 1;">
      <h3>Healthcare</h3>
      <p>Medical camps and health awareness.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("---")

# --- 8. DONATE SECTION ---
st.markdown("<h2 style='text-align: center;'>Donate Now</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your small help can make a big difference. Scan the QR code below or use our UPI ID to donate directly to our welfare account.</p>", unsafe_allow_html=True)

# Using Streamlit columns to perfectly center the QR code and bank info
col_spacer1, col_qr, col_info, col_spacer2 = st.columns([0.5, 1.5, 2, 0.5])
with col_qr:
    st.image("qr-code.jpeg", width=200)
with col_info:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### UPI ID: `ektawelfaretrust5531@sbi`")
    st.caption("Name: EKTA WELFARE TRUST")
    st.write("Accepted via GPay, Paytm, PhonePe, and BHIM UPI.")

st.write("---")

# --- 9. CONTACT FORM ---
st.markdown("<h2 style='text-align: center;'>Contact Us</h2>", unsafe_allow_html=True)

with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Your Name", placeholder="Enter your full name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    message = st.text_area("Your Message", placeholder="Write your message here...", height=150)
    
    # The submit button (Styled orange via CSS above!)
    submitted = st.form_submit_button("Send Message")
    
    if submitted:
        if not name or not email or not message:
            st.warning("⚠️ Please fill out all fields before sending.")
        elif sheet:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                sheet.append_row([timestamp, name, email, message])
                st.success(f"✅ Thank you {name}! Your message has been sent successfully.")
                st.balloons()
            except Exception as e:
                st.error("❌ Failed to send message. Please try again later.")

# --- 10. CUSTOM FOOTER ---
st.markdown("""
<div style="background: black; color: white; text-align: center; padding: 20px; border-radius: 10px; margin-top: 30px;">
    <p style="margin: 0;">© 2026 Ektamission NGO | All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)