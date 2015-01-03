import tweepy


consumer_key="AsKsbI1voZYyThuG3bXPfHl4O"
consumer_secret="dMc5jiJk3wlUjxYPznabpdFyzIrM17tkgWYewiBwr5hmQrG0YH"

access_token="236130731-NGzmfopeme3loaGr9FmtsMdAFoYa42NZvmTuEb9k"
access_token_secret="wWrslbfSGeZ280Wc1WHO0GsBujTWe2Ea2Moli7OfsM3bG"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
print(api.me().name)


search_results = tweepy.Cursor(api.search,
                           q="russia",
                           count=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items(5000)

tweets = [ tweet.text \
	for tweet in search_results]

import pickle
f = open("C:/tmp/russia5k.pickle", "wb")
pickle.dump(tweets, f)
f.close()
tweets = pickle.load(open("C:/tmp/russia5kFullTweets.pickle", "rb"))

def words(tweets):
	return [w for tweet in tweets for w in tweet.split()]

words = words(tweets)

import nltk
freq_dist = nltk.FreqDist(words)
freq_dist.most_common(50)

import re


def get_rt_sources(tweet):
	rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
	return [source.strip() for tuple in rt_patterns.findall(tweet) for source in tuple if source not in ("RT", "rt", "via", "VIA")]

all_tweeets = [tweet for tweet in search_results]

import networkx as nx

def build_graph_of_tweets(tweets):
	g = nx.DiGraph()
	for tweet in tweets:
		rt_sources = get_rt_sources(tweet.text)
		if not rt_sources: continue
		for rt_source in rt_sources:
			g.add_edge(rt_source, tweet.user.screen_name, {"tweet_id" : tweet.id})
	return g

len(list(nx.connected_components(g.to_undirected())))

sorted(nx.degree(g).values())

nx.drawing.write_dot(g, "C:/tmp/russia_results.dot")

def write_dot(g, out):
	dot = ['"%s" -> "%s" [tweet_id=%s]' % (n1.encode('UTF-8'), n2.encode('UTF-8'), g[n1][n2]['tweet_id']) for n1, n2, in g.edges()]
	pprint.pprint(dot)
	f = open(out, 'w')
	f.write('strict digraph {\n%s\n}' % (';\n'.join(dot),))
	f.close()