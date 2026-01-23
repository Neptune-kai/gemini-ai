from google import genai
import os 
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

# System message to define the persona
yn_instructions = ( "You are a YN. Respond only in AAVE slang. " "Keep responses casual and conversational." ) 

# Create chat session
chat = client.chats.create( 
    model="gemini-1.5-flash",
    history=[ 
        {
            "role": "system",
            "parts":[
            {"text": yn_instructions}
            ]
        }    
    ]
)

print("Wsg twin (Type 'exit' to leave the hood)")

while True: 
    user_input = input("You: ")
     
    if user_input.lower() == 'exit':
         print("See you unc!") 
         break
     
    try: 
         response = chat.send_message(
         parts=[{"text": user_input}]
         )
    except Exception as e:
        print("Error:", e) 
        chat = client.chats.create(
            model="gemini-1.5-flash",
            history=[
                {
                    "role": "system",
                    "parts": [{"text": yn_instructions}] 
                }
                ]
            )
         
uploaded = client.files.upload(
             file="C:\\Users\\S1806291\\Downloads\\Compsci26\\Compsci26\\gemini\\gemini-ai\\daigo.mp4" 
)
         
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=[ 
        uploaded,
        "Summarize this video. Then create a quiz with an answer key."
    ]
)
print("\n=== VIDEO SUMMARY & QUIZ ===\n")
print(response.text)