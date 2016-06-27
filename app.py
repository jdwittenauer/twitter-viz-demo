import os
import time
import numpy as np
from flask import *
from flask_socketio import *
from celery import Celery
from pattern.web import Twitter
from sklearn.externals import joblib

path = os.path.realpath('') + '/scripts/'
sys.path.append(path)


# Initialize and configure Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['SOCKETIO_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['BROKER_TRANSPORT'] = 'redis'
app.config['CELERY_ACCEPT_CONTENT'] = ['pickle']

# Initialize SocketIO
socketio = SocketIO(app, message_queue=app.config['SOCKETIO_REDIS_URL'])

# Initialize and configure Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Load sentiment classification model
vectorizer = joblib.load(path + 'vectorizer.pkl')
classifier = joblib.load(path + 'classifier.pkl')


def classify_tweet(tweet):
    """
    Classify a tweet with either a positive (1) or negative (-1) sentiment.
    """
    pred = classifier.predict(vectorizer.transform(np.array([tweet.text])))

    if pred[0] == 1:
        return '1'
    else:
        return '-1'


@celery.task
def create_stream(phrase, queue):
    """
    Celery task that connects to the twitter stream and runs a loop, periodically
    emitting tweet information to all connected clients.
    """
    local = SocketIO(message_queue=queue)
    stream = Twitter().stream(phrase, timeout=30)

    for i in range(100):
        stream.update()
        for tweet in reversed(stream):
            local.emit('tweet', {'id': str(i),
                                 'data': str(tweet.text.encode('ascii', 'ignore')),
                                 'sentiment': classify_tweet(tweet)})
        stream.clear()
        time.sleep(1)


@app.route('/', methods=['GET'])
def index():
    """
    Route that maps to the main index page.
    """
    return render_template('index.html')


@app.route('/twitter/<phrase>', methods=['POST'])
def twitter(phrase):
    """
    Route that accepts a twitter search phrase and queues a task to initiate
    a connection to twitter.
    """
    queue = app.config['SOCKETIO_REDIS_URL']
    create_stream.apply_async(args=[phrase, queue])
    return 'Establishing connection...'


if __name__ == '__main__':
    socketio.run(app, debug=True)
