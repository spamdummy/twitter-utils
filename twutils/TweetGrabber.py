#!/usr/bin/env python
#import sqlite3 as lite 
import logging
import os, json, Queue, tweepy
from threading import Thread

def getAuth(credentials):
	c = credentials
	auth = tweepy.OAuthHandler(c["CONSUMER_KEY"], c["CONSUMER_SECRET"])
	auth.set_access_token(c["ACCESS_TOKEN"], c["ACCESS_TOKEN_SECRET"])
	return auth

def loadCredential(_file):
	with open(_file) as f:
		j = json.load(f)
		if all(x in j for x in ("CONSUMER_KEY","CONSUMER_SECRET","ACCESS_TOKEN","ACCESS_TOKEN_SECRET")):
			return j			
		else:
			raise Exception("Credentials file", _file, "is not valid")


def getTweepyAPI(credentials):
	auth = getAuth(credentials)	
	return tweepy.API(auth)


class TweetGrabber(object):
	def __init__(self,credentials,worker,out_worker,populateQueue,threads_per_cred=2):
		'''
		** TweetGrabber **
		Note: A credential refers to a Twitter API Key
		This class enables multithreaded, multi-API-key usage of the Twitter REST API 
		through Tweepy
		credentials - a list of mappings in form of:
			{
			"CONSUMER_KEY":"XXXX",
			"CONSUMER_SECRET":"XXXX",
			"ACCESS_TOKEN":"XXXX",
			"ACCESS_TOKEN_SECRET":"XXXX"
			}
		worker - a function with the interface worker(worker_id,tweepy_api,queue_in,queue_out)
		
		out_worker - a function with the interface out_worker(queue_in,queue_out)				
		- This function should look something like this:
		...
		
		populateQueue - a function with the interface populateQueue(queue_in)
		
		threads_per_cred - number of threads to run with each credential
		'''
		self.threads_per_cred = threads_per_cred
		self.populateQueue = populateQueue
		self.credentials = []
		for cred in credentials:
			
			if cred in self.credentials:
				logging.warn("Duplicate credential CONSUMER_KEY = %s added." % cred["CONSUMER_KEY"])
			self.credentials.append(cred)
						
		self.worker = worker
		self.out_worker = out_worker
	

	def run(self):
		q = Queue.Queue()
		out_q = Queue.Queue()
		
		self.populateQueue(q)
		
		if q.empty():
			logging.info("No items to download")
			return

		
		count = 0			
		for cred in self.credentials:		
			for x in xrange(self.threads_per_cred):
				print "Adding worker %s - %s" % (count,cred["CONSUMER_KEY"])
				api = getTweepyAPI(cred)
				t = Thread(target=self.worker,args=(count,api,q,out_q))
				t.daemon = True
				t.start()
				count +=1
		
		self.out_worker(q,out_q)
		
if __name__ == "__main__":
	pass