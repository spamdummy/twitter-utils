# twitter-utils
Various utility functions for use with tweepy and the Twitter REST API

#What is TweetGrabber?
- TweetGrabber is a 'wrapper' for the Tweepy API.
- It lets you use multiple API Keys to interface with Tweepy and the Twitter REST API.


#TweetGrabber Prerequisites 
- Twitter Account
- At least one Twitter API Key
- Go [here](https://apps.twitter.com/) if you need to setup an API Key
- For each API Key make a plain text file in json format like so:
```
{
"CONSUMER_KEY":"XXXXXXX",
"CONSUMER_SECRET":"XXXXXXX",
"ACCESS_TOKEN":"XXXXXX",
"ACCESS_TOKEN_SECRET":"XXXXXXX"
}
```

#Usage
- Check out sample.py
- In the main function replace the cred_files tuple with the filenames of your API Key json files.


#Dependencies
- [tweepy](http://www.tweepy.org/)
- Python 2.7.5
