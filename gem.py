import os
import time
from google import genai
from google.genai import errors, types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('API_KEY'))

# Using Gemini 3 Flash for the fastest response times
MODEL_ID = "gemini-3-flash-preview"

# The "YN" Persona: Hype, AAVE, and knowledgeable about fighting games
yn_instructions = (
    "You are a YN. Respond only in AAVE. You are hosting a high-stakes quiz about "
    "the Daigo Parry (Evo Moment 37). Ask ONE question at a time. Wait for the user "
    "to answer. If they get it right, get hype! If they miss, clown them a bit. "
    "Use lingo like 'hitstun', 'full parry', 'super art', and 'punish'."
)

def start_interactive_quiz(file_path):
    video_file = None
    try:
        print(f"Uploading the tape: {file_path}...")
        video_file = client.files.upload(file=file_path)
        
        while video_file.state.name == "PROCESSING":
            print("AI is 'watching' the frames... stay solid...")
            time.sleep(15)
            video_file = client.files.get(name=video_file.name)

        # 90 second wait to refill the 'Token Bucket' for video
        print("Vid ready. Refilling gas for 90 seconds...")
        for i in range(90, 0, -10):
            print(f"Refilling... {i}s left")
            time.sleep(10)

        # Create the Chat Session
        chat = client.chats.create(
            model=MODEL_ID,
            config=types.GenerateContentConfig(
                system_instruction=yn_instructions
            )
        )

        print("\n--- 🥊 THE EVO MOMENT 37 CHALLENGE ---")
        
        # Start the convo by passing the video and the first prompt
        response = chat.send_message([video_file, "Yo, I'm ready. Start the quiz! Ask me the first question."])
        print(f"\nAI: {response.text}")

        # The interactive loop: respond to the AI until you type 'exit'
        while True:
            user_input = input("\nYour Answer (type 'exit' to quit): ")
            
            if user_input.lower() == 'exit':
                print("Peace out, twin. Stay in the lab.")
                break
                
            # Send your answer back to the chat
            response = chat.send_message(user_input)
            print(f"\nAI: {response.text}")

    except errors.ClientError as e:
        print(f"\n[!] Blocked: {e}")
    finally:
        if video_file:
            client.files.delete(name=video_file.name)
            print("\nCloud cleaned up. Session ended.")

if __name__ == "__main__":
    target = r"C:\Users\S1806291\Downloads\Compsci26\Compsci26\gemini\gemini-ai\digo.mp4"
    if os.path.exists(target):
        start_interactive_quiz(target)
    else:
        print(f"Can't find the file at {target}. Check your path!")