import time
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
# Make sure your .env file has API_KEY=your_actual_key
client = genai.Client(api_key=os.getenv('API_KEY'))

# Your custom persona instructions
yn_instructions = "You are a YN. Respond only in AAVE, using gangster slang and hood terms."

def create_video_quiz(file_path):
    print(f"Checking the tape at {file_path}... hold on twin.")
    
    # 1. Upload the video to the Google File API
    # This sends the MP4 from your computer to the AI's 'brain'
    video_file = client.files.upload(file=file_path)
    
    # 2. Wait for processing
    while video_file.state.name == "PROCESSING":
        print("AI watchin' the vid... stay patient...")
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("The vid didn't load right. Check the file format.")

    print("Vid loaded. Cookin' up the questions now.")

    # 3. The specific request for the AI
    prompt = "Watch this video and create a quiz with 5 challenging questions based on what happened. Include the answers at the end."
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[video_file, prompt],
        config={'system_instruction': yn_instructions}
    )

    return response.text

# --- THIS IS WHERE YOU PUT THE PATH ---
if __name__ == "__main__":
    # I used an 'r' before the quotes so Windows doesn't get confused by the backslashes
    target_video = r"C:\Users\S1806291\Downloads\Compsci26\Compsci26\gemini\gemini-ai\daigo.mp4"
    
    # This line triggers the whole process using the path above
    quiz_result = create_video_quiz(target_video)
    
    print("\n--- HERE IS YOUR QUIZ ---")
    print(quiz_result)