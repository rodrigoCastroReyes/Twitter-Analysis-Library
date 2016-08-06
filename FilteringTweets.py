# -*- coding: utf-8 -*-
import simplejson as json
import sys
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import string
from nltk.corpus import stopwords
from FileWorker import *
import unicodedata
import os

class FilteringTweets(object):
	"""docstring for FilteringTweets"""
	def __init__(self, tweets=None):
		super(FilteringTweets, self).__init__()
		self.tweets = tweets

	def getUsers(self):
		users = []
		for tweet in self.tweets:
			users.append(tweet["user"])
		return users

	def searchUsers(self,id):
		for user in self.users:
			if user["id"] == id:
				return user
		return None

	def getFreqTweetsOfUsers(self):
		ids = []
		for user in self.users:
			ids.append(user["id"])	
		return self.getFrequency(ids)
	
	def generateUsersCSV(self,fileName):
		listTuples = self.getFreqTweetsOfUsers()
		dataList = []
		i = 0
		for item in listTuples:
			userID, value = item
			user = self.searchUsers(userID)
			if user["friends_count"] != 0:
				ratio = float(user["followers_count"]) / float(user["friends_count"])
				line = "%d,%d,%s,%d,%d,%d,%.3f"%(i,user["id"],user["name"],user["friends_count"],user["followers_count"],value,ratio)
				dataList.append(line)
			i+=1
		self.fileWorker.writeFile(fileName,dataList)
		
	def getFrequency(self,items):#items can be list of users, words, hashtags
		freqs = {}
		for word in items:
			freqs[word] = freqs.get(word, 0) + 1 
		keys = list(freqs) #getKeys
		listTuples = []
		for key in keys:
			listTuples.append((key,freqs[key]))#(key,value)

		listTuples.sort(key=lambda tup: tup[1])
		listTuples.reverse()
		
		return listTuples #list ordered by frequency count

	def removeOutliers(self,threshold = 31):
		users_outliers = []
		filterTweets = []
		ids = []

		users = getUsers(self.tweets)
	
		for user in users:#get ids
			ids.append(user["id"])

		listTuples = getFrequency(ids)
		top = threshold
		#outliers are all the user who have published too many tweets in a short time
		#get users outliers
		for i in range(top):
			user , value = listTuples[i]
			users_outliers.append(user)

		for tweet in self.tweets:
			user = tweet["user"]["id"]
			if not(user in users_outliers):
				filterTweets.append(tweet)
		
		self.tweets = filterTweets;

	def removeSpammers(self,threshold=0.263):
		filterTweets = []
		for tweet in self.tweets:
			user = tweet["user"]
			ratio = 0.0000
			if user["friends_count"] != 0:
				ratio = float(user["followers_count"]) / float(user["friends_count"])
			if ratio > threshold :
				filterTweets.append(tweet)
		
		self.tweets = filterTweets;

	def inBoundingBox(self,tweet,min_lat = 1.465886, max_lat = 10.719366, min_lng = -71.818712, max_lng = -62.458360):
		"""
		SW : 1.465886, -71.818712
		NE : 10.719366, -62.458360
		"""
		lat = tweet["latitud"]
		lng = tweet["longitud"]
		return lat >= min_lat and lat <= max_lat and lng >= min_lng and lng <= max_lng

	def belongsToRegion(self,regions,tweet):
		for region in regions:
			points = region["points"]
			sw = points[0]
			ne = points[3]
			if self.inBoundingBox(tweet,sw[0],ne[0],sw[1],ne[1]):
				return region["id"]
		return None

	def isNoise(self,tweet,words_noise):
		flag = False
		for keyword in words_noise:	
			if re.search(keyword,tweet['text']):
				flag = True
				break
		return flag

	def filterByLocation(self):
		tweetsFilters = []
		for tweet in self.tweets:
			if self.inBoundingBox(tweet):
				tweetsFilters.append(tweet)
		self.tweets = tweetsFilters

	def generateRegions(self,k=3.33,num_cells=9):
		#x_init = 1.0
		#y_init = -62.0
		x_init = 42.2
		y_init = -2.2
		regions = []
		id_reg = 1

		for i in xrange(1,num_cells + 1):
			for j in xrange(1,num_cells + 1):
				region = {}
				region["id"] = id_reg
				points = []
				x1 = x_init + k*(j-1)
				y1 = y_init 
				points.append((x1, y1))
				points.append((x1, y1 + k))
				points.append((x1 + k, y1))
				points.append((x1 + k, y1 + k))
				region["points"] = points
				regions.append(region)
				id_reg += 1
			y_init = y_init + k

		return regions

	def splitDataByRegions(self,k = 2,num_cells = 5):
		regions = self.generateRegions(k,num_cells)
		splitTweets = {}

		for i in xrange(1,num_cells*num_cells + 1):
			splitTweets[i] = []

		cont = 1
		for tweet in self.tweets:
			region = self.belongsToRegion(regions,tweet)
			if region is not None:
				splitTweets[region].append(tweet)
			else:
				cont+=1
		print "perdida " + str(cont)
		return splitTweets

	def getTweets(self):
		return self.tweets
