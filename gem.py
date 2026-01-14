import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv('API_KEY'))

# System message to define the persona
yn_instructions = "You are a YN. Respond only in AAVE, using gangster slang and hood terms. Do not reply in normal English."

# Initialize the model with system instructions
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=yn_instructions
)

def start_chat():
    # Start a chat session to maintain context (optional but recommended)
    chat_session = model.start_chat(history=[])
    
    print("Wsg twin (Type 'exit' to leave the hood)")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("See you unc!")
            break
        
        try:
            # Send message to the model
            response = chat_session.send_message(user_input)
            print(f"\nPirate: {response.text}\n")
        except Exception as e:
            print(f"Blimey! An error occurred: {e}")

if __name__ == "__main__":
    start_chat()
