import streamlit as st 
import google.genai as genai 
import os 
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY")) 

st.set_page_config(page_title="Video Review AI", layout="centered") 

st.title("🎥 Video Review AI")

# Upload video
video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])
if video_file:
    st.video(video_file) 
    
    if st.button("Analyze Video"):
        with st.spinner("AI is reviewing the video..."): 
            
            client = genai.Client(api_key=os.getenv("API_KEY")) 
            uploaded = client.files.upload(file=video_file)
            
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            response = model.generate_content([ 
                uploaded, 
                "Summarize this video and create a quiz with answers."
            ])
        st.subheader("AI Review") 
        st.write(response.text)