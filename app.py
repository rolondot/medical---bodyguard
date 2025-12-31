import streamlit as st
from openai import OpenAI

# --- 1. CONFIGURATION & DESIGN ---
st.set_page_config(page_title="Medical Advocate", layout="centered")

# This CSS forces the "High-Tech Medical Chart" look
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117; /* Dark Slate Background */
        color: #FAFAFA;
    }
    .stSelectbox > div > div {
        background-color: #262730;
        color: white;
    }
    .stButton>button {
        width: 100%;
        background-color: #2DD4BF; /* Medical Teal */
        color: #000000;
        font-weight: bold;
        border: none;
        padding: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Make the success box look like a green console printout */
    .stSuccess {
        background-color: #064E3B;
        color: #6EE7B7;
        border-left: 5px solid #34D399;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE INTERFACE ---
st.title("🏥 MEDICAL ADVOCACY PROTOCOL")
st.markdown("`SYSTEM STATUS: ONLINE // ID: PT-894`")
st.divider()

# Input Grid
col1, col2 = st.columns(2)
with col1:
    pain = st.selectbox("PAIN LEVEL", ["Select...", "Mild", "Moderate", "Severe/Acute", "Intolerable"])
    duration = st.selectbox("DURATION", ["Select...", "New (Days)", "Sub-Acute (Weeks)", "Chronic (>3 Months)"])

with col2:
    impact = st.multiselect("FUNCTIONAL IMPACT", ["Sleep", "Work Ability", "Mobility", "Cognition", "Appetite"])
    goal = st.selectbox("GOAL", ["Select...", "Referral to Specialist", "Imaging/Testing", "Medication Adjustment", "Documentation Only"])

# --- 3. THE LOGIC ---
if st.button("GENERATE CLINICAL REPORT"):
    
    # Check if the user filled out the form
    if pain == "Select..." or goal == "Select...":
        st.error("❌ ERROR: INCOMPLETE DATA. Please select Pain Level and Goal.")
    
    # Check if the API Key is connected (Safety Check)
    elif "OPENAI_API_KEY" not in st.secrets:
        st.warning("⚠️ SYSTEM ALERT: OpenAI API Key missing. Please add it to Streamlit Secrets to generate text.")
    
    else:
        # If everything is good, run the AI
        try:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            # The Hidden "System Prompt" - You edit this to change the AI's personality
            system_instruction = """
            You are a medical advocate for a racialized neurodivergent patient. 
            Translate their inputs into strict, clinical, objective language. 
            Use short sentences. Do not be emotional. 
            If they want 'Documentation', explicitly ask the doctor to record any refusals in the chart.
            """
            
            user_data = f"Patient reports {pain} pain for {duration}. Impact: {impact}. Goal: {goal}."
            
            with st.spinner("PROCESSING CLINICAL TRANSLATION..."):
                # 1. Generate Text
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_data}
                    ]
                )
                script_text = response.choices[0].message.content
                
                # 2. Generate Audio (Voice)
                audio_response = client.audio.speech.create(
                    model="tts-1",
                    voice="onyx", # Deep, authoritative voice
                    input=script_text
                )
                
                # 3. Show Results
                st.success("✅ REPORT GENERATED")
                st.code(script_text, language="markdown") # Display text in a code box
                st.audio(audio_response.content, format="audio/mp3") # Audio player
                
        except Exception as e:
            st.error(f"SYSTEM FAILURE: {e}")
