import os
import sys
path = os.path.realpath('') + '/scripts/'
sys.path.append(path)

import time
import numpy as np
from flask import *
from flask_socketio import *
from celery import Celery, chain
from pattern.web import Twitter
from sklearn.externals import joblib
from gensim.models import Word2Vec
from tokenizer import *


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

# Load transforms and models
vectorizer = joblib.load(path + 'vectorizer.pkl')
classifier = joblib.load(path + 'classifier.pkl')
pca = joblib.load(path + 'pca.pkl')
word2vec = Word2Vec.load(path + 'word2vec.pkl')


def classify_tweet(tweet):
    """
    Classify a tweet with either a positive (1) or negative (0) sentiment.
    """
    pred = classifier.predict(vectorizer.transform(np.array([tweet.text])))

    return str(pred[0])


def vectorize_tweet(tweet):
    """
    Convert a tweet to vector space using a pre-trained word2vec model, then transform
    a sum of the vectorized words to 2-dimensional space using PCA to give a simple
    2D coordinate representation of the original tweet.
    """
    tweet_vector = np.zeros(100)
    for word in tokenize(tweet.text):
        if word in word2vec.vocab:
            tweet_vector = tweet_vector + word2vec[word]

    components = pca.transform(tweet_vector)
    x = components[0, 0]
    y = components[0, 1]

    return str(x), str(y)


@celery.task
def create_stream(phrase, queue):
    """
    Celery task that connects to the twitter stream and runs a loop, periodically
    emitting tweet information to all connected clients.
    """
    local = SocketIO(message_queue=queue)
    stream = Twitter().stream(phrase, timeout=30)

    for i in range(60):
        stream.update()
        for tweet in reversed(stream):
            sentiment = classify_tweet(tweet)
            x, y = vectorize_tweet(tweet)
            local.emit('tweet', {'id': str(i),
                                 'text': str(tweet.text.encode('ascii', 'ignore')),
                                 'sentiment': sentiment,
                                 'x': x,
                                 'y': y})
        stream.clear()
        time.sleep(1)

    return queue


@celery.task
def send_complete_message(queue):
    """
    Celery task that notifies the client that the twitter loop has completed executing.
    """
    local = SocketIO(message_queue=queue)
    local.emit('complete', {'data': 'Operation complete!'})


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
    # create_stream.apply_async(args=[phrase, queue])
    chain(create_stream.s(phrase, queue), send_complete_message.s()).apply_async()
    return 'Establishing connection...'


if __name__ == '__main__':
    socketio.run(app, debug=True)
