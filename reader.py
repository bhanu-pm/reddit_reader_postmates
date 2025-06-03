import os
from dotenv import load_dotenv
import json
from praw import Reddit
import boto3


s3_client = boto3.client('s3')
aws_bucket_name = "pcg-comment-storage"
file_name = "all_comments.json"

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
			file_content = s3_client.get_object(Bucket=aws_bucket_name, Key=file_name)["Body"].read().decode("utf-8")
			self.all_comments_list_json = json.loads(file_content)

		except Exception as e:
			self.all_comments_list_json = []


	def fetch_unseen_comments(self):
		# Stickied submission (Pinned post) obj
		subreddit_obj = self.reddit.subreddit(self.subreddit_name)
		submission_obj = subreddit_obj.sticky() ##########################
		# submission_obj = self.reddit.submission("1hqyk7y")
		# print(submission_obj)
		# print(type(submission_obj))

		submission_obj.comment_sort = "new"
		submission_obj.comments.replace_more(limit=None)

		unseen_comments_list = []
		for i, comment in enumerate(submission_obj.comments):
			# print(comment.body)
			unseen_comments_dict = {}
			if self.all_comments_list_json and comment.id == self.all_comments_list_json[0]["id"]:
				break
			unseen_comments_dict["id"] = comment.id
			unseen_comments_dict["body"] = comment.body
			unseen_comments_list.append(unseen_comments_dict)
			self.add_comment_to_dict(comment, i)

		return unseen_comments_list


	def add_comment_to_dict(self, comment, pos:int = 0):
		self.latest_comment_dict = {}
		self.latest_comment_dict["id"] = comment.id
		self.latest_comment_dict["body"] = comment.body
		self.all_comments_list_json.insert(pos, self.latest_comment_dict)


	def dump_to_json(self, file_name:str = file_name):
		s3_client.put_object(Bucket=aws_bucket_name, Key=file_name, Body=json.dumps(self.all_comments_list_json))


if __name__ == "__main__":
	# pass
	read_subreddit = Reader("postmates")
	unseen = read_subreddit.fetch_unseen_comments()

	for i in unseen:
		print(i)
	# print(unseen)
