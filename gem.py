import google.genai as genai
import os # Create client with API key

load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

# System message to define the persona
yn_instructions = ( "You are a YN. Respond only in AAVE slang. " "Keep responses casual and conversational." ) 

# Initialize the model with system instructions
model = genai.GenerativeModel( 
    model_name="gemini-1.5-flash", 
    system_instruction="..."
)
def start_chat():
    chat_session = model.start_chat(history=[]) 

print("Wsg twin (Type 'exit' to leave the hood)")
while True: 
    user_input = input("You: ")
     
    if user_input.lower() == 'exit':
         print("See you unc!") 
         break
    try: 
         response = chat_session.send_message(user_input)
         print(f"\nPirate: {response.text}\n")
    except Exception as e:
         print(f"Error: {e}") 
         
         # Start the persona chat
         start_chat() 
         
         #  --- VIDEO PROCESSING PART ---
         # Upload the video 
         myfile = client.files.upload(
             file="C:\\Users\\S1806291\\Downloads\\Compsci26\\Compsci26\\gemini\\gemini-ai\\daigo.mp4" 
             )
         # Use a model that supports video
         # video_model = genai.GenerativeModel("gemini-1.5-flash")
response = video_model.generate_content([ myfile, "Summarize this video. Then create a quiz with an answer key." ])
        
print(response.text)