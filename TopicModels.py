import math

class TopicModelingMetrics(object):
	"""docstring for TopicModelingMetrics"""
	def __init__(self):
		super(TopicModelingMetrics, self).__init__()
	
	def get_top(self,topic_words,n_topics):
		words = []
		for i, topic_dist in enumerate(topic_words):
			topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
			topic_words = [word.encode('utf-8') for word in topic_words]
			words += topic_words
			print('Topic {}: {}'.format(i, ' '.join(topic_words)))

	def get_idf_topic(self,topic_words,topic_k,word_v):
		num_topics = topic_words.shape[0]
		bkn = topic_words[topic_k][word_v]
		value = 1.0
		for topic_dist in topic_words:
			value = value*topic_dist[word_v]
		return math.log(1.0*bkn/math.pow(value,1.0/num_topics))
	
	def get_term_score(self,topic_words,topic_k,word_v):
		tf_topic = topic_words[topic_k][word_v]
		idf_topic = self.get_idf_topic(topic_words,topic_k,word_v)
		return tf_topic*idf_topic

	def get_highest_scores(self,topic_words,vocabulary,k_top=10):
		#topic_words = model.topic_word_
		num_topics = len(topic_words) 
		print "Numero de topicos",num_topics
		top_words = []

		for topic_k in range(num_topics):
			scores = []
			for v,word in enumerate(vocabulary):
				score = self.get_term_score(topic_words,topic_k,v)
				#print "score",score
				scores.append((word,score))
			scores.sort(key=lambda tup: tup[1]) 
			scores = scores[-k_top:]
			print "Topico %d"%(topic_k)
			for word,score in scores:
				print "%s,%.4f"%(word,score)
			print ""
			top_words += [ word for word,score in scores]

		return top_words