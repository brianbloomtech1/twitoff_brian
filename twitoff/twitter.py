from os import getenv
import not_tweepy as tweepy
from .models import DB, User, Tweet
import spacy

# get env variables
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# make connect to api
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)


def add_or_update_user(username):
    try:
        # 1) user info
        twitter_user = TWITTER.get_user(screen_name=username)
        # 2) check if already in database if not then creat new one
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, username=username))
        # 3) add the user to the database
        DB.session.add(db_user)
        # 4) get the user's tweets (in a list)
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)
        # 5) add all the individual tweets to database
        # since the last time user tweeted
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error Processing {username}: {e}")
        raise e

    else:
        # 6) committ
        DB.session.commit()

# take tweet text and turn it into a word num vector
nlp = spacy.load('my_model/')
# same tool as in flask shell
# give the function a test it returns word vec


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector





# ------- ------------------#
"""

# what should the key be???

'''take a username and pull data and tweets.
if user already exists
check for new tweets'''


def add_or_update_user(username):
    try:
        # 1) user info
        twitter_user = TWITTER.get_user(screen_name=username)
        # 2) check if already in database if not then creat new one
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, username=username)
        # 3) add the user to the database
        DB.session.add(db_user)
        # 4) get the user's tweets (in a list)
        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode='extended',
                                       since_id=db_user.newest_tweet_id)
        # update the newest tweet_id if there have been new tweets
        # since the last time user tweeted
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # 5) add all the individual tweets to database
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             vect=tweet_vector,
                             user_id=db_user.id)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e
    else:
        # 6) save the changes to the database
        DB.session.commit()






"""