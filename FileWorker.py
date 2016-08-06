from TweetParser import *
import simplejson as json
import sys
import os
import numpy as np

class FileWorker(object):

	json_dir_output = "/home/rodrigo/Twitter Analysis Library/outputs/json"
	txt_dir_output = "/home/rodrigo/Twitter Analysis Library/outputs/txt"

	def read(self,filename):#read a text file
		array = []
		with open(filename) as file:
			for line in file:
				line = line.rstrip('\r')
				line = line.rstrip('\n')
				array.append(line)
		return array

	def readJSON(self,filename):#read a json file
		with open(filename) as file:
			data = json.load(file)
			return data

	def writeJSON(self,filename,data):#write data like json file
		try:
			jsondata = json.dumps(data, indent=4, skipkeys=True, sort_keys=True)
			filename = os.path.join(self.json_dir_output,filename)
			fd = open(filename, 'w')
			fd.write(jsondata)
			fd.close()
			print filename + " ha sido escrito exitosamente"
		except Exception,e:
			print e
			print 'ERROR writing', filename
			pass

	def write(self,filename,dataList):# write data like .txt file
		filename = os.path.join(self.txt_dir_output,filename)
		fd = open(filename,mode='w+')
		for item in dataList:
			try:
				line = "%s\n"%(item)
				fd.write(line)
			except:
				print item
				pass
		fd.close()
		print filename + " ha sido escrito exitosamente"

	def saveMatrix(self,filename,matrix,items):
		dataList = []
		line = ""

		for item in items:
			line += "%s,"%(item)
		dataList.append(line.encode('utf-8'))

		i = 0 
		for vector in matrix:
			#line = "%s"%(items[i])
			line = ""
			for x in np.nditer(vector):
				line = line + "%f,"%(x)
			dataList.append(line.encode('utf-8'))	
			i+=1

		self.write(filename,dataList)


class TweetFileWorker(FileWorker):

	def writeTweets(self,filename,tweets_raw,fields,hashtagsFlag = True, mentionsFlag= True, ulrsFlag = True):
		tweets_processed =[]
		tweet_parser = TweetParser(fields,hashtagsFlag,mentionsFlag,ulrsFlag)

		for tweetRaw in tweets_raw:
			tweet = tweet_parser.parser(tweetRaw)
			tweets_processed.append(tweet)
		data = {}
		data["tweets"] = tweets_processed
		data["num_tweets"] = len(tweets)
		self.writeJSON(filename,data)


	def readRaw(self,filename,fields,hashtagsFlag = True, mentionsFlag= True, ulrsFlag = True):
		"""
		lee los tweets en bruto, se filtran los parametros especificados en fields
		si coordinates = True se incluyen campos lat y lng
		si user = True se agrega informacion de los usuarios
		"""
		data = self.readJSON(filename) #data debe contenter un campo con arreglo tweets
		tweets_raw = data["tweets"]
		tweets_processed =[]
		tweet_parser = TweetParser(fields,hashtagsFlag,mentionsFlag,ulrsFlag)

		for tweetRaw in tweets_raw:
			tweet = tweet_parser.parser(tweetRaw)
			tweets_processed.append(tweet)

		return tweets_processed


	def writeCSV(self,filename,tweets,fields):
		linesCSV = []
		line = ""

		for field in self.fields:
			line = line + field + ","
		linesCSV.append(line)

		for tweet in tweets:
			line = ""
			for field in fields:
				line = line + str(tweet[field]) + ","
			linesCSV.append(line)
		
		self.write(filename,linesCSV)


