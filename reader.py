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
			with open('codes.json', 'r') as file:
				self.comment_dict = json.load(file)

		except Exception as e:
			self.comment_dict = {}
			print(f"Error occured: {e}")

	def fetch_comment_tree(self):
		# Stickied submission (Pinned post) obj
		subreddit_obj = self.reddit.subreddit(self.subreddit_name)
		submission_obj = subreddit_obj.sticky()
		submission_obj.comment_sort = "new"
		submission_obj.comments.replace_more(limit=None)
		
		for comment in submission_obj.comments:
			print(comment)

	def get_latest_unseen_comment(self):
		pass


if __name__ == "__main__":
	read_subreddit = Reader("postmates")
	read_subreddit.fetch_comment_tree()
