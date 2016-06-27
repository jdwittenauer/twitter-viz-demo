import os
import time
from flask import *
from flask_socketio import *
from celery import Celery, chain

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


@celery.task
def add(x, y):
    return x + y


@celery.task
def multiply(x, y):
    return x * y


@celery.task
def generate_message(message, queue):
    time.sleep(1)
    local = SocketIO(message_queue=queue)
    local.emit('task complete', {'data': 'The answer is: {0}'.format(str(message))})


@app.route('/message', methods=['GET'])
def message():
    return render_template('message.html')


@app.route('/submit/<int:x>/<int:y>', methods=['POST'])
def submit(x, y):
    queue = app.config['SOCKETIO_REDIS_URL']
    chain(add.s(x, y), multiply.s(10), generate_message.s(queue)).apply_async()
    return 'Waiting for a reply...'


if __name__ == '__main__':
    socketio.run(app, debug=True)
