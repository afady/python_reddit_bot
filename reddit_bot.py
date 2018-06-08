import praw
import prawcore
import config
import time
import os
import random
import constants

sleep_duration = 30
comments_to_pull = 5000
subreddit_to_pull = 'popular'
reddit_account = 'your_reddit_account'
search_word = 'fady'

def bot_login():
	print("\n\n\n\nLogging in...\n")
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = reddit_account)
	print ("Logged in!\n")
	return r

def run_bot(r):
	search_words_found = 0
	timeout_duration = 60
	time.ctime()
	current_time = time.strftime("%I:%M%p")
	print(current_time + " Reading "+str(comments_to_pull)+" comments.\n")

	try:
		for comment in r.subreddit(subreddit_to_pull).comments(limit=comments_to_pull):
			if search_word in comment.body and comment.id not in comments_replied_to and not comment.author == r.user.me():
				print("Search word found in comment " + comment.id)
				randomSleepTime = random.randint(10, 20)
				
				print("Sleeping for " + str(randomSleepTime) + " seconds.")
				time.sleep(randomSleepTime)

				comment.reply(random.choice(constants.reply_strings))
				search_words_found+=1
				comments_replied_to.append(comment.id)

				# save comment id so we dont reply to it again
				with open("comments_replied_to.txt", "a") as f:
					f.write(comment.id + "\n")

		if search_words_found == 0:
			print("Nothing found on that round.\n")
		else:
			print("Found "+str(search_words_found)+" instances of the search word.\n")

		print("Sleeping for "+str(sleep_duration)+" seconds.\n")
		print("\n-------------\n")
		time.sleep(sleep_duration)

	except (Exception) as e:
		eStr = str(e)
		if "RATELIMIT" in eStr:
			timeout_duration = [int(s) for s in eStr.split() if s.isdigit()][0]
			if "minutes" in eStr:
				# multiply by 60 to convert minutes to seconds
				timeout_duration *= 60
		print(e)
		print("\nSleeping for "+str(timeout_duration)+" seconds.\n")
		time.sleep(timeout_duration)
		run_bot(r)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
	return comments_replied_to

r = bot_login()

comments_replied_to = get_saved_comments()

while True:
	run_bot(r)