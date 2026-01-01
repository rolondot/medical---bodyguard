import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Medical Advocate", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stSelectbox > div > div { background-color: #262730; color: white; }
    .stButton>button {
        width: 100%; background-color: #2DD4BF; color: #000000;
        font-weight: bold; border: none; padding: 15px;
    }
    .stSuccess { background-color: #064E3B; color: #6EE7B7; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTERFACE ---
st.title("🏥 MEDICAL ADVOCATE (Free Version)")
st.markdown("`SYSTEM STATUS: ONLINE // ID: PT-894`")
st.divider()

col1, col2 = st.columns(2)
with col1:
    pain = st.selectbox("PAIN LEVEL", ["Select...", "Mild", "Moderate", "Severe/Acute", "Intolerable"])
    duration = st.selectbox("DURATION", ["Select...", "New (Days)", "Sub-Acute (Weeks)", "Chronic (>3 Months)"])
with col2:
    impact = st.multiselect("FUNCTIONAL IMPACT", ["Sleep", "Work Ability", "Mobility", "Cognition", "Appetite"])
    goal = st.selectbox("GOAL", ["Select...", "Referral to Specialist", "Imaging/Testing", "Medication Adjustment", "Documentation Only"])

# --- 3. LOGIC ---
if st.button("GENERATE CLINICAL REPORT"):
    
    if "GROQ_API_KEY" not in st.secrets:
        st.error("⚠️ KEY MISSING: Please add GROQ_API_KEY to secrets.")
    elif pain == "Select..." or goal == "Select...":
        st.error("❌ ERROR: Please fill all fields.")
    else:
        try:
            # A. THE BRAIN (Groq - Free)
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            system_instruction = """
            You are a medical advocate. Translate user inputs into strict, clinical language. 
            Use short sentences. Be firm and objective.
            If 'Documentation' is requested, explicitly ask the doctor to record any refusals in the chart.
            """
            
            user_data = f"Patient reports {pain} pain for {duration}. Impact: {impact}. Goal: {goal}."
            
            with st.spinner("PROCESSING (Free Tier)..."):
                completion = client.chat.completions.create(
                    model="llama3-8b-8192", # This is a fast, free, open-source model
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_data}
                    ],
                    temperature=0.5,
                )
                script_text = completion.choices[0].message.content
                
                # B. THE VOICE (gTTS - Free)
                # We save the audio to a temp file then play it
                tts = gTTS(text=script_text, lang='en', slow=False)
                tts.save("speech.mp3")
                
                # C. DISPLAY
                st.success("✅ REPORT GENERATED")
                st.code(script_text, language="markdown")
                
                # Play the audio file we just created
                audio_file = open('speech.mp3', 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
        except Exception as e:
            st.error(f"SYSTEM FAILURE: {e}")
