import os
import sys
path = os.path.realpath('') + '/scripts/'
sys.path.append(path)

import numpy as np
import pandas as pd
from sklearn.decomposition.pca import PCA
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from gensim.models import Word2Vec
from tokenizer import *


def main():
    print('Reading in data file...')
    data = pd.read_csv(path + 'Sentiment Analysis Dataset.csv',
                       usecols=['Sentiment', 'SentimentText'], error_bad_lines=False)

    print('Pre-processing tweet text...')
    corpus = data['SentimentText']
    vectorizer = TfidfVectorizer(decode_error='replace', strip_accents='unicode',
                                 stop_words='english', tokenizer=tokenize)
    X = vectorizer.fit_transform(corpus.values)
    y = data['Sentiment'].values

    print('Training sentiment classification model...')
    classifier = MultinomialNB()
    classifier.fit(X, y)

    print('Training word2vec model...')
    corpus = corpus.map(lambda x: tokenize(x))
    word2vec = Word2Vec(corpus.tolist(), size=100, window=4, min_count=10, workers=4)
    word2vec.init_sims(replace=True)

    print('Fitting PCA transform...')
    word_vectors = [word2vec[word] for word in word2vec.vocab]
    pca = PCA(n_components=2)
    pca.fit(word_vectors)

    print('Saving artifacts to disk...')
    joblib.dump(vectorizer, path + 'vectorizer.pkl')
    joblib.dump(classifier, path + 'classifier.pkl')
    joblib.dump(pca, path + 'pca.pkl')
    word2vec.save(path + 'word2vec.pkl')

    tweet = data['SentimentText'][0]
    tweet_vector = np.zeros(100)
    for word in tokenize(tweet):
        if word in word2vec.vocab:
            tweet_vector = tweet_vector + word2vec[word]
    components = pca.transform(tweet_vector)
    x = components[0, 0]
    y = components[0, 1]

    print('Process complete.')


if __name__ == "__main__":
    main()
