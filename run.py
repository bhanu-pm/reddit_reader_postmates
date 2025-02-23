import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from reader import Reader


load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if Query.GEMINI_KEY is None:
	raise EnvironmentError("GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_KEY)

def query(chat: list, model: str = "gemini-1.5-flash"):
	assert type(chat[0]["parts"]) == list, "Verify the chat format conforms to the model's requirements."
	g_model = genai.GenerativeModel(model)
	try:
		output = g_model.generate_content(chat)
		return output
	except Exception as e:
		print(f"Error: {e}")

