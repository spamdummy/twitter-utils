# twitter-utils (twutils)
Various utility functions for use with tweepy and the Twitter REST API. 
Contains the TweetGrabber class.

##What is TweetGrabber?
- TweetGrabber is a 'wrapper' for the Tweepy API.
- It lets you use multiple API Keys to interface with Tweepy and the Twitter REST API.


##Prerequisites 
- Twitter Account
- At least one Twitter API Key
Go [here](https://apps.twitter.com/) if you need to setup an API Key
For each API Key make a plain text file in json format like so:

```
{
"CONSUMER_KEY":"XXXXXXX",
"CONSUMER_SECRET":"XXXXXXX",
"ACCESS_TOKEN":"XXXXXX",
"ACCESS_TOKEN_SECRET":"XXXXXXX"
}
```
- Replace each item with your API Key's details

##Usage
- Use sample.py as a template for using this module. 

##Example
- Run sample.py, feeding the filenames of your API Key files as command line arguments
- For example if I have a single API Key stored in a file called key1.json, I would run the script like this:
```
python sample.py key1.json
```

##Notes
- Many improvements can be made to this code. 
- Further abstraction is definitely needed in the structure of the user supplied functions 'worker' and 'out_worker'

##Dependencies
- [tweepy](http://www.tweepy.org/)
- Python 2.7
