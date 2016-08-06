# -*- coding: utf-8 -*-
import simplejson as json
import sys
import re
import re
import string
import unicodedata
import os
from geopy.geocoders import Nominatim
from time import sleep

class TweetParser(object):
	"""docstring for TweetParser
	Recibe un tweet en bruto y retorna un tweet con una representación más ligera
	Se especifican fields: atributos del tweet los cuales pueden ser ['id','created_at','retweet_count','favorite_count']
	Se especifica si se desar incluir hashtags, mentions y urls
	Informacion de geolocalizacion y del usuario se incluye por defecto
	"""

	def __init__(self, fields, **kwargs):
		super(TweetParser, self).__init__()
		self.fields = fields
		self.mentionsFlag = kwargs['mentionsFlag']
		self.hashtagsFlag = kwargs['hashtagsFlag']
		self.urlsFlag = kwargs['urlsFlag']
		self.userFlag = kwargs['userFlag']
		self.coordinatesFlag = kwargs['coordinatesFlag']
		self.placeFlag = kwargs['placeFlag']

	def parse(self,rawTweet):
		tweet = {}

		for field in self.fields:
			tweet[field] = rawTweet[field]

		if self.mentionsFlag:
			tweet["mentions"] = self.getMentions(rawTweet)

		if self.hashtagsFlag:
			tweet["hashtags"] = self.getHashtags(rawTweet)
		
		if self.urlsFlag:
			tweet["urls"] = self.getUrls(rawTweet)

		if self.userFlag:
			tweet["user"] = self.getUser(rawTweet)

		if self.coordinatesFlag:
			tweet["coordinates"] = self.getCoordinates(rawTweet)

		if self.placeFlag:
			tweet['place'] = self.getPlace(rawTweet)

		return tweet


	def getUser(self,rawTweet,fields=['id','screen_name','lang','followers_count','friends_count','statuses_count']):
		user = {}
		for field in fields:
			user[field] = rawTweet["user"][field]
		return user

	def getCoordinates(self,rawTweet):
		coordinates = {}
		if rawTweet["coordinates"]:
			coordinates["longitud"] = rawTweet["coordinates"]["coordinates"][0]
			coordinates["latitud"] = rawTweet["coordinates"]["coordinates"][1]
		return coordinates

	def getMentions(self,rawTweet):
		mentions = []
		mentionsData = rawTweet["entities"]["user_mentions"]
		if len(mentionsData)>0:
			for mention in mentionsData:
				mentions.append(mention["screen_name"])
		return mentions

	def getHashtags(self,rawTweet):
		hashtags = []
		hashtagsData = rawTweet["entities"]["hashtags"]
		if len(hashtagsData)>0:
			for hashtag in hashtagsData:
				hashtags.append(hashtag["text"].lower())
		return hashtags

	def getUrls(self,rawTweet):
		urls = []
		urlsData = rawTweet["entities"]["urls"]
		if len(urlsData)>0:
			for url in urlsData:
				urls.append(url["url"])
		return urls

	def getPlace(self,rawTweet):
		place = {}
		if rawTweet['place']:
			place['country'] = rawTweet['place']['country']
			place['bounding_box'] = rawTweet['place']['bounding_box']
			place['name'] = rawTweet['place']['name']

		return place
