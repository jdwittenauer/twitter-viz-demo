import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from tokenizer import *

path = os.path.realpath('') + '/scripts/'
sys.path.append(path)


def main():
    print('Reading in data file...')
    data = pd.read_csv(path + 'Sentiment Analysis Dataset.csv',
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

    print('Saving transform/model to disk...')
    joblib.dump(vectorizer, path + 'vectorizer.pkl')
    joblib.dump(classifier, path + 'classifier.pkl')

    print('Process complete.')


if __name__ == "__main__":
    main()
