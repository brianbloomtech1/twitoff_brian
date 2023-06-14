from flask_sqlalchemy import SQLAlchemy

# create DB object SQLAlchemy class

DB = SQLAlchemy()  # create DB connection and inherit class


# special parent class DB.model for inherit
class User(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column
    username = DB.Column(DB.String, nullable=False)
    # most recent tweet id
    newest_tweet_id = DB.Column(DB.BigInteger)
    # backref as-if added tweets list to user class
    # tweets = []  # username plus list ID

    # def __repr__(self):
    #     return f"User: {self.username}"


class Tweet(DB.Model):
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text column
    text = DB.Column(DB.Unicode(300), nullable=False)
    # store our word embeddings "vectorization"
    vect = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # user column two way link between user object and tweet
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    # lazy only executes when needed
    # odd example here but make user tweets inslide the class

    # def __repr__(self):
    #     return f"Tweet: {self.text}"
