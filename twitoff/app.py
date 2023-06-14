from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user


def create_app():
    # create app factory function to export entire folder
    app = Flask(__name__)  # instantiates app

    # database configurations - where does the file live???
    # UR"I" not UR"L" and THREE SLASHES!!
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    # register our database with the app
    DB.init_app(app)
    # make sure they are fully connected and pass the app

    # my_var = "Twitoff App" # template demo not in use anymore

    @app.route('/')  # home route
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    # @app.route('/populate') just for testing
    # def populate():
    #     # create user
    #     add_or_update_user('nasa')
    #     return render_template('base.html', title='Populate')

    @app.route('/update')
    def update():
        # get list of usernames of all users
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title='Users Updated')
        # list comprehension version
        # for username in [user.username for user in users]:
        #    add_or_update_user(username)

    @app.route('/iris')
    def iris():    
        from sklearn.datasets import load_iris
        from sklearn.linear_model import LogisticRegression
        X, y = load_iris(return_X_y=True)
        clf = LogisticRegression(random_state=0, solver='lbfgs',
                                 multi_class='multinomial').fit(X, y)

        return str(clf.predict(X[:2, :]))

    @app.route('/reset')
    def reset():
        # drop all tables make according to new schema
        DB.drop_all()
        # recreate according to schema in models.py
        DB.create_all()
        return render_template('base.html', title='Database Reset')

    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):

        username = username or request.values['user_name']

        try:
            if request.method == 'POST':
                add_or_update_user(username)
                message = f'User "{username}" has been successfully added!'

            tweets = User.query.filter(User.username==username).one().tweets
        
        except Exception as e:
            message = f"Error adding {username}: {e}"
            tweets = []

        return render_template('user.html', title=username, tweets=tweets, message=message)


    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])
        hypo_tweet_text = request.values['tweet.text']
        if user0 == user1:
            message = 'Cannot compare a user to themselves'
        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)
            #get into the if statement if predicted user 1
            if prediction:
                message = f'"{hypo_tweet_text}" is more likely to be said by {user1} than by {user0}'
            else:
                message = f'"{hypo_tweet_text}" is more likely to be said by {user0} than by {user1}'

        return render_template('prediction.html', title='Prediction', message=message)
    
    return app

# demo notes
# outermost twitoff folder
# flask run 
