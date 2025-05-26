import os
from dotenv import load_dotenv
import json
from praw import Reddit

# import time
# from datetime import datetime
# from praw.models import MoreComments, Submission, Subreddit


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
			with open('all_comments.json', 'r') as file:
				self.all_comments_list_json = json.load(file)

		except FileNotFoundError:
			self.all_comments_list_json = []


	def fetch_unseen_comments(self):
		# Stickied submission (Pinned post) obj
		subreddit_obj = self.reddit.subreddit(self.subreddit_name)
		submission_obj = subreddit_obj.sticky()
		print(submission_obj)

		submission_obj.comment_sort = "new"
		submission_obj.comments.replace_more(limit=None)

		unseen_comments_list = []
		for comment in submission_obj.comments:
			unseen_comments_dict = {}
			if self.all_comments_list_json and comment.id == self.all_comments_list_json[0]["id"]:
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
		self.all_comments_list_json.insert(0, self.latest_comment_dict)

	def dump_to_json(self, file_name:str = "all_comments.json"):
		with open(file_name, "w") as file:
			json.dump(self.all_comments_list_json, file, indent=4)


if __name__ == "__main__":
	read_subreddit = Reader("postmates")
	unseen = read_subreddit.fetch_unseen_comments()

	for i in unseen:
		print(i['body'])
	# print(unseen)
