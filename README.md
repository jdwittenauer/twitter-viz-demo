# Twitter Visualization Demo
Experiment using various python-based technologies.  Initial version still in-progress!

## Quick Setup

- Clone this repository
- Install dependencies
- Open a terminal window and start a local Redis server ('bash redis.sh')
- Open another terminal window and start a Celery worker ('celery worker -A app.celery --loglevel=info')
- Open a third terminal window and start the Flask application ('python app.py')
- Browse to the app at 'http://localhost:5000/'
