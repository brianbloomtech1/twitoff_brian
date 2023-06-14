from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import vectorize_tweet


def predict_user(user0_username, user1_username, hypo_tweet_text):
    # Grab the users from the DB
    user0 = User.query.filter(User.username==user0_username).one()
    user1 = User.query.filter(User.username==user1_username).one()

    # Get the word embeddings from each other
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # vertical stack 2D numpy arrays into X matrix (the vects)
    X_train = np.vstack([user0_vects, user1_vects])

    # concatenate our labels of 0 or 1 for each tweet
    zeros = np.zeros(user0_vects.shape[0])
    ones = np.ones(user1_vests.shape[0])

    y_train = np.concatenate([zeros, ones])

    # one shot instantiate and fit
    log_req = LogisticRegression().fit(X_train, y_train)
    # lol that's the whole code to put machine learning into api
    # normally do beforehand in a notebook then put in proj

    # if possible then load and predict alraeady
    # in our case export training parameters and put in a file

    # vectorize held in 2d numpy not 1d
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text).reshape(1, -1)

    return log_req.predict(hypo_tweet_vect)[0]

    # user User users username screenname
    # test
    # # from twitoff.models import User
    # # from twitoff.predict import predict_user
    # # user0 = User.query.filter(User.username=='ryanallred').one()
    # # user1 = User.query.filter(User.username=='nasa').one() 
    # # hypo_tweet_text = "nasa is blah blah blah blah"
    # # one() is like fetchall
    # # predict_user(user0.username, user1.username, hypo_tweet_text)
    # jinga2 moving variables between the web and python
    