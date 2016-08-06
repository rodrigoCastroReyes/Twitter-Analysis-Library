import numpy as np
import datetime

class DateHelper(object):
	"""docstring for DateHelper"""
	def __init__(self):
		super(DateHelper, self).__init__()
	
	def getYear(self,date_text):
		year = datetime.datetime.strptime(date_text,'%a %b %d %H:%M:%S +0000 %Y').year
		return year	

	def getHour(self,date_text):
		hour = datetime.datetime.strptime(date_text,'%a %b %d %H:%M:%S +0000 %Y').hour
		return hour

	def getDay(self,date_text):
		year = datetime.datetime.strptime(date_text,'%a %b %d %H:%M:%S +0000 %Y').day
		return year	


class Helper(object):
	"""docstring for Helper"""

	def __init__(self):
		super(Helper, self).__init__()
	
	def getCoocurrenceMatrix(self,items,tweets,field):#field can be: hashtag,mention,tokens
		matrix = np.zeros( (len(items) , len(tweets)) )
		i=0
		# filas, columnas
		for item in items:
			j = 0
			print item
			for tweet in tweets:
				if item in tweet[field] :
					matrix[i,j] = 1
				j+=1
			i+=1
		return np.dot(matrix,matrix.transpose())

	def getTopItems(self,items,n = 5,threshold=1):
		freqs = self.getFrequency(items,threshold)
		i = 0
		
		ranked_items = []

		for index,tuple in enumerate(freqs):
			ranked_items.append(tuple)#(key,value)
			if i == n :
				break
			i+=1
				
		return ranked_items


	def getFrequency(self,items,threshold):#items can be list of users, words, hashtags
		freqs = {}

		for word in items:
			freqs[word] = freqs.get(word, 0) + 1 
		
		keys = list(freqs) #getKeys
		
		listTuples = []
		
		for key in keys:
			if freqs[key] > threshold:
				listTuples.append((key,freqs[key]))#(key,value)

		listTuples.sort(key=lambda tup: tup[1])
		listTuples.reverse()
		
		return listTuples #list ordered by frequency count

	def drawBarChart(self,x,x_labels,y,title,bar_width = 0.8):
		opacity = 0.4
		fig_size = plt.rcParams["figure.figsize"]# Get current size
		# Set figure width to 12 and height to 9
		fig_size[0] = 12
		fig_size[1] = 9
		plt.rcParams["figure.figsize"] = fig_size
		rects1 = plt.bar(x,y,bar_width,alpha=opacity,color='b')
		plt.ylabel('Scores')
		plt.title(title)
		plt.xticks(x + 0.35,x_labels,rotation='vertical',fontsize='small')
		plt.legend()
		plt.show()

