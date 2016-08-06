# -*- coding: utf-8 -*-
import hunspell
from FileWorker import *
from nltk.stem.snowball import SnowballStemmer

class StemmerSpanish(object):

	def __init__(self):
		super(StemmerSpanish, self).__init__()
		#self.stemmer = SnowballStemmer(lang)
		self.hobj = hunspell.HunSpell('/home/rodrigo/Twitter Analysis Library/lib/hunspell/Spanish.dic', 
			'/home/rodrigo/Twitter Analysis Library/lib/hunspell/Spanish.aff')
		self.load_stemming_words()

	def apply(self,tokens):
		text_array = []
		for word in tokens:
			word = self.stemming(word)
			text_array.append(word)
		return text_array	

	def stemming(self,word):
		if word in self.stemmingWords["words"]:
			index = self.stemmingWords["words"].index(word)
			wordMatch = self.stemmingWords["matches"][index]
			return wordMatch
		else:
			stem = self.hobj.stem(str(word));
			if stem:
				#print self.hobj.analyze(str(word))
				word = stem[0]
			return word

	def load_stemming_words(self):
		#load a set of knowing words
		self.stemmingWords = {}
		self.stemmingWords["words"] = []
		self.stemmingWords["matches"] = []
		fileWorker = FileWorker()
		data = fileWorker.read("/home/rodrigo/Twitter Analysis Library/lib/db/stemmingDataBase.csv")
		for word in data:
			attr = word.split(',')
			word = attr[0]
			match = attr[1].rstrip()
			self.stemmingWords["words"].append(word)
			self.stemmingWords["matches"].append(match)