# Author: Deana Del Vecchio
# File: twitterstream_public.py
# Purpose: Gather n amount of tweets, subtract English words, and then tag each word based on its part of speech (POS).
# Words will then be pulled from the stored words to form "MadLib" type sentences.
# Work in progress.

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from collections import defaultdict
import nltk
import time

ckey = ' ENTER YOURS '
csecret = ' ENTER YOURS '
atoken = ' ENTER YOURS '
asecret = ' ENTER YOURS '
words = defaultdict(set)

class listener(StreamListener):
    Counter = 0
    saveFile = open('twitDB3.csv','w') #overwrites existing file
    saveFile.close()   
    def on_data(self, data):           
        try:
            n = 100
            if listener.Counter >= n:
                return False # exits once n tweets have been gathered
        tweetlang =data.split(',"lang":"')[1].split('","contributors_enabled')[0] # future: filter before gather
            if 'en' in tweetlang:
                saveFile = open('twitDB3.csv','a') # appends to file; future: MYSQL for Database storage?
                tweet = data.split(',"text":"')[1].split('","source')[0]
                saveFile.write(tweet)
                saveFile.write('\n')
                saveFile.close()
                listener.Counter+=1
            return True
        except BaseException, e:
            print 'failed ondata ',str(e)
            time.sleep(5)

    def on_error(self, status):
        print status

def WordFilter(text):
    keepers=""
    text = text.replace('\n',' ') ##### I don't think this is working 
    text = text.split()
    for words in text: # filters out "non words"
        if '@' in words or \
           '#' in words or \
           'RT' in words or \
           'http' in words or \
           '\u' in words:
            continue
        else:
            keepers = keepers + " " + words # probably better way to do this; FUTURE FIX
    return keepers

auth = OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["a","the","of","an","and","your","#"]) # search for these words, commas = or

print "Has tweets" # for my benefit. Will remove at some point.

saveFile = open('twitDB3.csv','r') # future fix

for line in saveFile:
    line = WordFilter(line)   
    text = nltk.word_tokenize(line)
    textpos = nltk.pos_tag(text) # Look into other ways for POS tagging
    for value,key in textpos:
        words[key].add(value)
saveFile.close()

print words.keys() # Future fix: look into merging broad POS

print "done" # for my benefit; Remove in fututure
