import os
from dotenv import load_dotenv
import time
from datetime import datetime
import json

from praw import Reddit
from praw.models import MoreComments, Submission, Subreddit


class Reader:
	# Reddit user object
	load_dotenv()
	client_id = str(os.getenv("CLIENT_ID"))
	client_secret = str(os.getenv("CLIENT_SECRET"))
	user_agent = "postmates_reader by me"

	def __init__(self, subreddit_name="postmates"):
		self.reddit = Reddit(client_id=Reader.client_id, client_secret=Reader.client_secret, user_agent=Reader.user_agent)
		self.subreddit_name = subreddit_name
		try:
			with open('final_comments.json', 'r') as file:
				self.comments_list_json = json.load(file)

		except Exception as e:
			self.comments_list_json = []
			print(f"Error occured: {e}")

	def fetch_unseen_comments(self):
		# Stickied submission (Pinned post) obj
		subreddit_obj = self.reddit.subreddit(self.subreddit_name)
		submission_obj = subreddit_obj.sticky()
		submission_obj.comment_sort = "new"
		submission_obj.comments.replace_more(limit=None)
		
		unseen_comments_list = []
		unseen_comments_dict = {}
		for comment in submission_obj.comments:
			if comment.id == self.comments_list_json[0]["id"]:
				break
			unseen_comments_dict["id"] = comment.id
			unseen_comments_dict["body"] = comment.body
			unseen_comments_list.append(unseen_comments_dict)

		return unseen_comments_list

	def add_comment_to_dict(self, comment, location: str, code: str):
		self.latest_comment_dict = {}
		self.latest_comment_dict["id"] = comment.id
		self.latest_comment_dict["body"] = comment.body
		self.latest_comment_dict["location"] = location
		self.latest_comment_dict["code"] = code
		self.comments_list_json.insert(0, self.latest_comment_dict)

	def dump_to_json(self, file_name:str = "final_comments.json"):
		with open(file_name, "w") as file:
			json.dump(self.comments_list_json, file, indent=4)


if __name__ == "__main__":
	read_subreddit = Reader("postmates")
	read_subreddit.fetch_comment_tree()
