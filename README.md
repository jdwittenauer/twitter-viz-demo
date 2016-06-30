# Twitter Visualization Demo
Experiment using various python-based technologies.  Initial version still in-progress!

## Quick Setup

- Clone this repository
- Install dependencies (Flask, Flask-SocketIO, Redis, Celery, Pattern, Numpy, Pandas, Scikit-learn, Gensim)
- Download twitter sentiment dataset [here](http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip)
- Unzip the .csv file and save a copy in the 'scripts' folder
- Run 'build_models.py' from the 'scripts' folder (can take a while on a slower machine)
- Open a terminal window and start a local Redis server ('bash redis.sh')
- Open another terminal window and start a Celery worker ('celery worker -A app.celery --loglevel=info')
- Open a third terminal window and start the Flask application ('python app.py')
- Browse to the app at 'http://127.0.0.1:5000/'