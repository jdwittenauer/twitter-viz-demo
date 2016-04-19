from flask import *
from celery import Celery, chain

# Initialize and configure Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['BROKER_TRANSPORT'] = 'redis'


# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def add(x, y):
    return x + y


@celery.task
def multiply(x, y):
    return x * y


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        x = int(request.form['x'])
        y = int(request.form['y'])
        chain(add.s(x, y), multiply.s(10)).apply_async()
        flash('Added {0} and {1} together and multiplied by 10!'.format(x, y))
        return redirect(url_for('index'))


@app.route('/submit/<int:x>/<int:y>', methods=['POST'])
def submit(x, y):
    result = add.apply_async((x, y))
    return str(result.get())


@app.route('/hello/', methods=['GET'])
@app.route('/hello/<name>', methods=['GET'])
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
