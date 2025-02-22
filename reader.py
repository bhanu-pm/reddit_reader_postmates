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

	def fetch_comment_tree(self):
		# Stickied submission (Pinned post) obj
		subreddit_obj = self.reddit.subreddit(self.subreddit_name)
		submission_obj = subreddit_obj.sticky()

		top_level_comments = submission_obj.comments

		for comment in top_level_comments:
			print(comment)
			print(type(comment))


if __name__ == "__main__":
	read_subreddit = Reader("postmates")
	read_subreddit.fetch_comment_tree()
