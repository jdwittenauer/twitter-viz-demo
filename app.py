from flask import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret'


@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)  # http://127.0.0.1:5000/
