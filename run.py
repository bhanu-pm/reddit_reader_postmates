# import google.generativeai as genai
from google import genai
from dotenv import load_dotenv
import os
import time
from reader import Reader
import re


load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if Query.GEMINI_KEY is None:
	raise EnvironmentError("GEMINI_API_KEY not found")

genai.configure(api_key=GEMINI_KEY)

def query(chat: list, model: str = "gemini-2.0-flash"):
	# assert type(chat[0]["parts"]) == list, "Verify the chat format conforms to the model's requirements."
	# g_model = genai.GenerativeModel(model)
	# try:
	# 	output = g_model.generate_content(chat)
	# 	return output
	# except Exception as e:
	# 	print(f"Error: {e}")

	prompt = """I will give you a list of chat messages that were written by people. These messages are generally
    	written to share a postmates coupon code along with how much it is worth and in what locations it would work.
    	There might also be some cases where people only post the codes and no other details about it.

    	I will be giving you a list of such messages, your job is to understand what is written in the message,
    	parse it and rewrite it in the following form/structure.

    	[|#code#, #location#, #value#|, |#code#, #location#, #value#|]

    	Here, the pipe sign | should encapsulate the details of one message and each detail should be encapsulated
    	within a pound/hashtag sign #. The overall set of messages should be encapsulated within the square brackets
    	[]. 

    	Here are a few examples on how you should format it from the messages. 
    	1. LETSGOGCU Phoenix $20 off
    	2. Code: NYEPUBCRAWL

Las Vegas Only!

$20 Off!
        3. $15 off $20 Postmates code!

LA Only!

Code: 2025GIFT
        4. Letsgo49ers

$20 off. Charlotte only. Don't add it if you don't live in that area. It will apply to your account but the promo won't apply when you try to check out.
        
        [|#LETSGOGCU#, #Phoenix#, #20#|, |#NYEPUBCRAWL#, #Las Vegas#, #20#|, |#2025GIFT#, #LA#, #15#|, |#Letsgo49ers#, #Charlotte#, #20#|]

        You can add more pipe symbols and increase the size of the final set of list based on the messages I give you.
        The next messages will be the messages you should parse and return according to the above given format.
        Just return the parsed message list and nothing else.\n	"""
	messages_txt = ""
	for i, j in enumerate(chat):
		messages_txt += f"{i+1}. {j}\n"

	final_prompt = prompt + messages_txt
	client = genai.Client(api_key=GEMINI_KEY)

	response = client.models.generate_content(
    	model=model,
    	contents=final_prompt,
	)
	print(response.text)
	return response.text

def get_comments():
	comments = read.fetch_unseen_comments()
	comment_list = []
	for i in comments:
		comment_list.append(i)

	return comment_list

read = Reader("postmates")
comment_list = get_comments()
response_text = query(comment_list)


