import os
import sys

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    sys.path.append(os.getcwd() + '\\scripts')

import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from tokenizer import *


def main():
    print('Reading in data file...')
    dir = 'C:\\Users\\jdwittenauer\\Documents\Git\\twitter-viz-demo\\scripts\\'
    data = pd.read_csv(dir + 'Sentiment Analysis Dataset.csv',
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

    print('Saving model to disk...')
    f = open(dir + 'classifier.pkl', 'wb')
    pickle.dump(classifier, f)
    f.close()

    print('Process complete.')


if __name__ == "__main__":
    main()
