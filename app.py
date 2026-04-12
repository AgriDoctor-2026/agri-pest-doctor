import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuration
genai.configure(api_key="AIzaSyDCCviYQMnGdUlXGA7vLzR4OmfmJDK8Gpc")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI Layout
st.set_page_config(page_title="Agri Doctor Pro", page_icon="🐛")

# Sidebar for Language Selection (Logic)
lang_option = st.sidebar.selectbox("Select Language", ["English", "Tamil"])

# 3. Translation Dictionary (English Coding Strings)
ui_data = {
    "English": {
        "title": "Agri Doctor Pro",
        "pay_msg": "Subscription Required",
        "pay_info": "Please pay 10 rupees using the QR code below.",
        "pay_done": "I have paid",
        "success": "Verified!",
        "upload": "Upload Image",
        "loc": "Enter Location",
        "analyze": "Analyze",
        "loading": "Wait...",
        "result": "Result",
        "error": "API Error"
    },
    "Tamil": {
        "title": "Agri Doctor Pro (Tamil Version)",
        "pay_msg": "Intha sevaiyai payanpadutha 10 rubai seluthavum",
        "pay_info": "Kile ulla QR code-ai scan seiyavum",
        "pay_done": "Nan panam seluthi vitten",
        "success": "Sari paarkkapattathu!",
        "upload": "Pugaippadathai etravum",
        "loc": "Oorin peyar",
        "analyze": "Aaraichi sei",
        "loading": "Kaathiru...",
        "result": "Mudivugal",
        "error": "API Pilai"
    }
}

st.title(ui_data[lang_option]["title"])

# --- 4. Payment Implementation ---
if 'status_paid' not in st.session_state:
    st.session_state.status_paid = False

if not st.session_state.status_paid:
    st.subheader(ui_data[lang_option]["pay_msg"])
    st.write(ui_data[lang_option]["pay_info"])
    
    # Static link to your QR code on GitHub
    st.image("https://raw.githubusercontent.com/AgriDoctor-2026/agri-pest-doctor/main/qr_code.png", width=300)
    
    if st.button(ui_data[lang_option]["pay_done"]):
        st.session_state.status_paid = True
        st.success(ui_data[lang_option]["success"])
        st.rerun()
    st.stop()

# --- 5. Main App Logic ---
user_loc = st.text_input(ui_data[lang_option]["loc"], "Tamil Nadu")
pest_file = st.file_uploader(ui_data[lang_option]["upload"], type=["jpg", "png", "jpeg"])

if pest_file is not None:
    img_data = Image.open(pest_file)
    st.image(img_data, use_container_width=True)
    
    if st.button(ui_data[lang_option]["analyze"]):
        with st.spinner(ui_data[lang_option]["loading"]):
            try:
                # Prompt logic (AI responds in the selected language)
                if lang_option == "Tamil":
                    final_prompt = f"Identify this pest. Give details in TAMIL ONLY for location {user_loc}."
                else:
                    final_prompt = f"Identify this pest. Give details in ENGLISH ONLY for location {user_loc}."
                
                ai_res = model.generate_content([final_prompt, img_data])
                st.success(ui_data[lang_option]["result"])
                st.write(ai_res.text)
            except:
                st.error(ui_data[lang_option]["error"])

st.markdown("---")
st.caption("Developed by AgriDoctor-2026")

