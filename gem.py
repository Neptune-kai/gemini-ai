import os
import time
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('API_KEY'))

MODEL_ID = "gemini-2.0-flash-lite" 
yn_instructions = "You are a YN. Respond only in AAVE, using gangster slang and hood terms."

def create_video_quiz_safe(file_path):
    print(f"Checking the tape at {file_path}... stay solid.")
    
    # 1. Upload
    video_file = client.files.upload(file=file_path)
    
    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)

    prompt = "Create a 5-question quiz based on this video with answers at the end."

    # 2. Smart Retry Logic (Backoff)
    max_retries = 3
    wait_time = 30 # Start with 30 seconds

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[video_file, prompt],
                config={'system_instruction': yn_instructions}
            )
            # Cleanup: Clear the cloud storage
            client.files.delete(name=video_file.name)
            return response.text
            
        except errors.ClientError as e:
            if "429" in str(e):
                if attempt < max_retries - 1:
                    print(f"\n[!] Federal block. Too many requests. Cooling down for {wait_time}s...")
                    time.sleep(wait_time)
                    wait_time *= 2 # Wait longer next time
                    continue
                else:
                    return "Yo, the ceiling is too low right now. Try again in a few minutes, twin."
            raise e

if __name__ == "__main__":
    # Fixed the .mp4.mp4 issue from before
    target_video = r"C:\Users\S1806291\Downloads\Compsci26\Compsci26\gemini\gemini-ai\digo.mp4"
    
    if os.path.exists(target_video):
        print(create_video_quiz_safe(target_video))
    else:
        print(f"Yo, I still can't find the file at: {target_video}")