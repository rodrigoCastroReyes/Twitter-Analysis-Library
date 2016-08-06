import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import linalg
from sklearn import cluster
from FileWorker import *

class TweetsTFFIDFModel(object):
	"""docstring for AnalystTweets"""
	def __init__(self,corpus_tweets,features):
		super(TweetsTFFIDFModel, self).__init__()
		self.corpus = corpus_tweets
		self.features = features
		self.matrix = None

	def transform(self):
		self.vectorizer = TfidfVectorizer(min_df=1, vocabulary=self.features, norm = 'l2')
		self.matrix = self.vectorizer.fit_transform(self.corpus).todense()

	def save_in_file(self,filename):
		linesCSV = []
		line = ""
		for features in self.features:
			line = line + features + ","

		linesCSV.append(line)
		for vector in self.matrix:
			mag = np.linalg.norm(vector,ord=1)
			if mag > 0.0 :
				line = ""
				for x in np.nditer(vector):
					line = line + "%.4f,"%(x)
				linesCSV.append(line)
		
		worker = FileWorker()
		worker.write(filename+".csv",linesCSV)

