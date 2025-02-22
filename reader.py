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
			with open('comments.json', 'r') as file:
				self.comments_list_json = json.load(file)

		except Exception as e:
			self.comments_list_json = []
			print(f"Error occured: {e}")

	def fetch_comment_tree(self):
		# Stickied submission (Pinned post) obj
		subreddit_obj = self.reddit.subreddit(self.subreddit_name)
		submission_obj = subreddit_obj.sticky()
		submission_obj.comment_sort = "new"
		submission_obj.comments.replace_more(limit=None)
		
		for comment in submission_obj.comments:
			print(f"Default: {comment}")
			print(f"ID: {comment.id}")
			print(f"Body: {comment.body}")
			print(" ################################################### ")

	def get_latest_unseen_comment(self):
		pass

	def add_comment_to_dict(self, comment, location: str, code: str):
		self.latest_comment_dict = {}
		self.latest_comment_dict["id"] = comment.id
		self.latest_comment_dict["body"] = comment.body
		self.latest_comment_dict["location"] = location
		self.latest_comment_dict["code"] = code
		self.comments_list_json.insert(0, self.latest_comment_dict)

if __name__ == "__main__":
	read_subreddit = Reader("postmates")
	read_subreddit.fetch_comment_tree()
