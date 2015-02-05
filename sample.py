#!/usr/bin/env python
import tweepy
import twutils
import time
import logging


def getUserTimeline(tweepy_api,id,count=1):
	"""
	Returns a hash of tweetIDs mapped 
	to tweet raw json  
	1 <= count <= 200
	"""
	api = tweepy_api
	out = {}
	for tweet in tweepy.Cursor(api.user_timeline,id=id).items(count):
		out[tweet.id_str] = tweet._json
	return out

def worker(worker_id,tweepy_api,queue_in,queue_out):
	while not queue_in.empty():
		item = queue_in.get()
		#logging.info("In %s" % item)
		
		tweets = getUserTimeline(tweepy_api,item,count=1)
		
		queue_out.put(tweets)
		queue_in.task_done()



def doContinue(queue_in,queue_out):	
	return not queue_in.empty() or not queue_out.empty() or queue_in.unfinished_tasks>0
	
def out_worker(queue_in,queue_out):
	try:
		while doContinue(queue_in,queue_out):
			if queue_out.empty():
				#Wait some time before checking the queue again...
				time.sleep(2) 
			else:
				tweets = queue_out.get()
				
				#We now have the tweets...
				#As an example we can print the tweets to the screen
				#Remember that the tweet is just a mapping object.
				for tweetID, tweet in tweets.items():
					logging.info("User ID: %s" % tweet["user"]["id"])
					logging.info(tweet["text"])

				#Add some code to store the tweets.
				#Maybe use an SQLite database or 
				#maybe Pickle the data...
				pass

				queue_out.task_done()

	except (KeyboardInterrupt, SystemExit), e:
		#Handle an interrupt here.

		#If you want to make sure you store everything in the 'out queue'
		#before the program exits, do something like this:
		while not queue_out.empty():
			item = queue_out.get()
			
			#code to store item goes here...
			pass
			
			queue_out.task_done()
			
		return

def populateQueue(queue):
	userIDs = {
		"WIRED": 1344951,
		"Ed Yong": 19767193,
		"CERN": 15234407,
	}
	for id in userIDs.values():
		queue.put(id) 


def main():
	credentials = []	
	cred_files = ("acc1.json",)
	for _file in cred_files:
		credentials.append(twutils.loadCredential(_file))
	
	g = twutils.TweetGrabber(credentials,worker,out_worker,populateQueue,threads_per_cred=1)
	g.run()
	
if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()
	