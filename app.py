import time
from flask import *
from flask_socketio import *
from celery import Celery, chain


# Initialize and configure Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['SOCKETIO_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['BROKER_TRANSPORT'] = 'redis'

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


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit/<int:x>/<int:y>', methods=['POST'])
def submit(x, y):
    queue = app.config['SOCKETIO_REDIS_URL']
    chain(add.s(x, y), multiply.s(10), generate_message.s(queue)).apply_async()
    return 'Waiting for a reply...'


@app.route('/hello/', methods=['GET'])
@app.route('/hello/<name>', methods=['GET'])
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    socketio.run(app, debug=True)
