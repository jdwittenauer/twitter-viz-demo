import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    sys.path.append(os.getcwd() + '\\scripts')

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from tokenizer import *


data_dir = 'C:\\Users\\jdwittenauer\\Documents\Git\\twitter-viz-demo\\scripts\\'


def main():
    print('Reading in data file...')
    data = pd.read_csv(data_dir + 'Sentiment Analysis Dataset.csv',
                       usecols=['Sentiment', 'SentimentText'], error_bad_lines=False)

    print('Pre-processing tweet text...')
    corpus = data['SentimentText'].values
    vectorizer = TfidfVectorizer(decode_error='replace', strip_accents='unicode',
                                 stop_words='english', tokenizer=tokenize)
    X = vectorizer.fit_transform(corpus)
    y = data['Sentiment'].values

    print('Training sentiment classification model...')
    classifier = MultinomialNB()
    classifier.fit(X, y)
    print('complete')

    y_pred = classifier.predict(X)

    label_names = ['Negative', 'Positive']
    print(classification_report(y, y_pred, target_names=label_names))

    print('Process complete.')


if __name__ == "__main__":
    main()
