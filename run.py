from google import genai
from dotenv import load_dotenv
import os
import time
from reader import Reader
import json
import re


load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_KEY is None:
	raise EnvironmentError("GEMINI_API_KEY not found")

client = genai.Client(api_key=GEMINI_KEY)

def query(chat: list, model: str = "gemini-2.0-flash"):
	prompt = """I will give you a list of chat messages that were written by people. 
	These messages are generally written to share coupon codes along with how much it is worth 
	and in what locations it would work.

	There might also be some cases where people only post the codes and no other details about it. 
	Sometimes there might be messages like this [deleted], it just means that the message 
	has been deleted, you can ignore them while parsing.

	I will be giving you a list of such messages, your job is to understand what is written in the message, 
	parse it and rewrite it in a python json format with the code being stored in the "code" key 
	and location stored in the "location" key and value stored in the "value" key.
	Just return the parsed message and nothing else. Put all the parsed messages in the same json object,
	so in essense you just output a single json object (a list of dicts) with each dict in the list containing 
	details about one message. The next messages will be the messages you should parse and 
	return according to the instructions I gave you. \n"""

	messages_txt = ""
	for i, j in enumerate(chat):
		messages_txt += f"{i+1}. {j['body']}\n"

	final_prompt = prompt + messages_txt

	response = client.models.generate_content(
    	model=model,
    	contents=final_prompt,
	)
	# print(final_prompt)
	print(response.text)
	return response.text

def get_comments():
	comments = read.fetch_unseen_comments()
	comment_list = []
	for i in comments:
		comment_list.append(i)

	return comment_list

def parse_output(out:str):
	match = re.search(r"```json\s*(.*?)\s*```", out, re.DOTALL | re.IGNORECASE)
	result = match.group(1).strip()
	# print(result)
	json_out = json.loads(result)
	return json_out

def check_relevance(json_obj:list):
	for i in json_obj:
		if (i["location"] is None) or ("boston" in i["location"].lower()):
			pass


read = Reader("postmates")
comment_list = get_comments()
if len(comment_list) > 0:
	response_text = query(comment_list)
	output = parse_output(response_text)

	print(output)
	print(type(output))
