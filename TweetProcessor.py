#!/usr/bin/env python
# coding=utf-8
import sys
import re
import string
import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
from pattern.es import lemma,singularize
from pattern.en import tag
from unidecode import unidecode
from FileWorker import *
from StemmerSpanish import *
reload(sys) 
sys.setdefaultencoding('utf-8')

class BreakerUpWords(object):
	"""docstring for ProcessorEntities"""
	def __init__(self):
		super(BreakerUpWords, self).__init__()
		self.worker = FileWorker()
		self.load_words_codes()
		
	def load_words_codes(self):
		self.words_codes = {}
		self.words_codes["words"] = []
		self.words_codes["codes"] = []
		data = self.worker.read("/home/rodrigo/Twitter Analysis Library/lib/db/hashtagsDataBase.csv")
		for item in data:
			attr = item.split(',')
			word = attr[0]
			code = attr[1]
			self.words_codes["words"].append(word)
			self.words_codes["codes"].append(code)

	def save_words_codes(self):
		num_codes = len(self.words_codes["words"])
		lines = []
		for i in range(num_codes):
			word = self.words_codes["words"][i]
			code = self.words_codes["codes"][i]
			line = "%s,%s"%(word,code)
			lines.append(line)
		self.worker.write("hashtagsDataBase.csv",lines)

	def break_up_words(self,tokens):
		new_tokens = []
		for token in tokens:
			new_tokens = new_tokens + self.break_up(token)				
		return new_tokens

	def break_up(self,token):
		tokens = []
		if token in self.words_codes["words"]:#if toke is words_codes so we will break up token
			index = self.words_codes["words"].index(token)
			code = self.words_codes["codes"][index]
			token = self.segment(token,code)#break up the words with the specified code
			for newToken in token:
				tokens.append(newToken)
			return tokens
		else:
			return [token]

	def segment(self,text,segs):
		words = []
		last = 0
		for i in range(len(segs)):
			if segs[i] == '1':
				words.append(text[last:i+1])
				last = i+1
		words.append(text[last:])
		return words

class TextProcessor(object):

	def __init__(self):
		super(TextProcessor, self).__init__()
		self.stemmer = StemmerSpanish()
		self.breaker = BreakerUpWords()

	def remove_accents(self,text):
		#text = unicodedata.normalize('NFD', text).encode('ascii','ignore')
		stripped = u"".join([c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)])
		return stripped

	def remove_hashtags(self,text):
		regex = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)" # hash-tags
		text = re.sub(regex,' ',text)
		return text

	def remove_mentions(self,text):
		regex = r'@[^\s]+'#remove @-mentions
		text = re.sub(regex,' ',text)
		return text

	def remove_urls(self,text):
		regex = r'http\S+'#remove url
		text = re.sub(regex,' ',text)
		regex = r'htt'#remove url
		text = re.sub(regex,' ',text)
		return text

	def remove_punctuation(self,text):
		# r'[.]',#remove points
		regex = r'[%s]' % re.escape(string.punctuation)#signsPattern
		text = re.sub(regex,' ',text)
		return text
	"""
	def remove_emoji(self,text):
		emoji_pattern = re.compile("["
			u"\U0001F600-\U0001F64F"  # emoticons
			u"\U0001F300-\U0001F5FF"  # symbols & pictographs
			u"\U0001F680-\U0001F6FF"  # transport & map symbols
			u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
			u"\U00002600-\U000026FF"#symbolsPattern
			"]+", flags=re.UNICODE)
		return emoji_pattern.sub(r'', text)
	"""

	def remove_emoji(self,data):
	    """
	    去除表情
	    :param data:
	    :return:
	    """
	    if not data:
	        return data
	    if not isinstance(data, basestring):
	        return data
	    try:
	    # UCS-4
	        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
	    except re.error:
	    # UCS-2
	        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
	    return patt.sub('', data)


	def remove_special_issues(self,text):
		regex_issues = [
			r'jaja*',
			r'jeje*',
			r'[0-5][7-9]*',
			r'\n'
		]
		for regex in regex_issues:
			text = re.sub(regex,' ',text)
		return text

	def remove_stop_words(self,tokens,other_words = []):
		#receive a list of tokens return a list without stopwords
		#you can include your custom words into other_words array
		#other_words = ['rt','caracas','mrida','maracaibo','gran','asi','hoy','si']
		stop = stopwords.words('spanish')
		stop = stop + other_words
		return [token for token in tokens if token not in stop]

	def remove_enlongations(self,text):
		re.sub(r'a*','a',text)
		re.sub(r'e*','e',text)
		re.sub(r'i*','i',text)
		re.sub(r'o*','o',text)
		re.sub(r'u*','u',text)
		return text
	"""
	def stemming(self,tokens):
		return self.stemmer.apply(tokens)
	"""
	def stemming(self,tokens):
		text = " ".join(tokens)
		words = []
		part_of_speech = {}
		part_of_speech['noun'] = ["NN"]
		part_of_speech['verbs'] = ["VB","VBG","VBP","VBZ","VBN","VBD"]
		part_of_speech['plural'] = ["NNS"]
		part_of_speech['adjective'] = ["JJ"]
		for word, pos in tag(text):
			if pos in part_of_speech['noun']:
				word = self.stemmer.stemming(word)
			if pos in part_of_speech["verbs"]:			
				word = lemma(word)
			if pos in part_of_speech['plural']:
				word = singularize(word)
			if pos in part_of_speech['adjective']:
				word = self.stemmer.stemming(word)
			words.append(word)
		return words

	def tokenization(self,text):
		#this function pre-process de text of a tweet return a list of tokens
		tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
		text = text.lower()# text to lower
		text = text.rstrip('\n')
		text = self.remove_urls(text)#remove urls
		text = self.remove_punctuation(text)#remove sign puntuation
		text = self.remove_emoji(text)
		text = self.remove_special_issues(text)
		tokens = word_tokenize(text)
		#tokens = tknzr.tokenize(text)
		#print text.decode('utf-8')
		tokens = self.breaker.break_up_words(tokens)#rompe palabras que estan unidas ejm: venezuelaquierecambio
		tokens = map(self.remove_accents,tokens)
		tokens = map(self.remove_enlongations,tokens)
		tokens = self.remove_stop_words(tokens)#remove stop words

		tokens_re = re.compile( r'(?:[\w_]+)', re.VERBOSE | re.IGNORECASE)
		tokens_str = " ".join(tokens)
		tokens = tokens_re.findall(tokens_str)
		tokens = self.stemming(tokens)
		tokens = [token for token in tokens if len(token)>2]

		return tokens

class TweetProcessor(object):

	"""docstring for ProcessorTweets"""
	def __init__(self):
		super(TweetProcessor, self).__init__()
		self.processor = TextProcessor()

	def process(self,text,rm_mentions=False,rm_hashtags=False):
		if rm_mentions:
			text = self.processor.remove_mentions(text)
		if rm_hashtags:
			text = self.processor.remove_hashtags(text)
		tokens = self.processor.tokenization(text)
		return tokens