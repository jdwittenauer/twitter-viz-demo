# Twitter Visualization Demo

![twitter-viz-demo](https://raw.githubusercontent.com/jdwittenauer/twitter-viz-demo/master/example.png)

This project leverages a variety of technologies to visualize a real-time stream of twitter data using sentiment analysis and word vector space mapping via word2vec.  It runs on a local Flask instance with a Redis/Celery back-end and uses Socket-IO to push events to the web client.  Twitter integration is managed by the pattern library.  NVD3 is used on the front-end to create the visualization.

## Quick Setup Instructions

- Clone this repository
- Install dependencies (Flask, Flask-SocketIO, Redis, Celery, Pattern, Numpy, Pandas, Scikit-learn, Gensim)
- Download twitter sentiment dataset [here](http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip)
- Unzip the .csv file and save a copy in the 'scripts' folder
- Run 'build_models.py' from the 'scripts' folder (can take a while on a slower machine)
- Open a terminal window and start a local Redis server ('bash redis.sh')
- Open another terminal window and start a Celery worker ('celery worker -A app.celery --loglevel=info')
- Open a third terminal window and start the Flask application ('python app.py')
- Browse to the app at 'http://127.0.0.1:5000/'