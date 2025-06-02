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
read = Reader("postmates")

def query(chat: list, model: str = "gemini-2.0-flash"):
	prompt = """I will give you a list of chat messages that were written by people. 
	These messages are generally written to share coupon codes along with how much it is worth 
	and in what locations it would work.

	There might also be some cases where people only post the codes and no other details about it. 
	Sometimes there might be messages like this [deleted] or [removed], it just means that the message 
	has been deleted, you can ignore them while parsing.

	I will be giving you a list of such messages, your job is to understand what is written in the message, 
	parse it and rewrite it in a python json format with the code being stored in the "code" key 
	and location stored in the "location" key and price stored in the "price" key.

	If no location is provided or if the location provided is in the state of Massachusetts of USA or if the
	location provided works in all of USA, put "MA" in the "location" key. For all other locations put their 
	respective locations in the "location" key. If there is no price just put "0" in the "price" key.

	Here is an example: message= BOBA25 $15 Phoenix.
	Here, the code is BOBA25, and $15 is the price, and Phoenix is the location (since in this case it doesn't make much sense to be talking about the phoenix bird lol).

	Maintain the order of the messages in the json object. Put all the parsed messages in the same json object,
	so in essense you just output a single json object (a list of dicts) with each dict in the list containing 
	details about one message. The next messages will be the messages you should parse and 
	return according to the instructions I gave you. It is of the utmost importance that you give the final json
	object at the end of all of your thinking and the json object should be enclosed by ```json and ```.
	Here is an example:
	```json
	[
	{
	code: "BOBA25",
	location: "Phoenix",
	price: "15"
	}
	]
	```
	Think step by step, but don't output too much jargon.\n"""

	messages_txt = ""
	for i, j in enumerate(chat):
		messages_txt += f"{i+1}. {j['body']}\n"

	final_prompt = prompt + messages_txt

	response = client.models.generate_content(
    	model=model,
    	contents=final_prompt,
	)
	# print(final_prompt)
	# print(response.text)
	return response.text

def get_comments():
	comments = read.fetch_unseen_comments()
	comment_list = []
	for i in comments:
		comment_list.append(i)

	return comment_list

def parse_output(out:str):
	match = re.search(r"```json(.*?)```", out, re.DOTALL)
	result = match.group(1).strip()
	# print(f"Parsed result is :\n{result}")
	json_out = json.loads(result)
	return json_out

def check_relevance(json_obj:list):
	temp = []
	for i, j in enumerate(json_obj):
		if "MA" in j['location']:
			# print(j)
			temp.append(j)
	return temp


def lambda_handler(event, context):
	# TODO implement
	comment_list = get_comments()
	if len(comment_list) > 0:
		read.dump_to_json()
		response_text = query(comment_list)
		output = parse_output(response_text)
		# print(f"Output: {output}")
		final_output = check_relevance(output)
		# print("Here are the codes")

		return {
        		'statusCode': 200,
        		'body': final_output
    		}
	else:
		# print("No new comments")
		return {
        		'statusCode': 200,
        		'body': json.dumps('No new comments!')
    		}


out = lambda_handler("hi", "hi")
print(out)
