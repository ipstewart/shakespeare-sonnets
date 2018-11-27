
""" 

poetry_slam.py
by Ian Stewart

Generated shakespearean sonnets using language and sentence structure from 
Shakespeare's original sonnets. Sonnets are generated and scored based on
how well they follow the rhyme scheme, meter, and syllable count. Sonnets are
analyzed for tone and read allowed by the terminal according to their tone.

"""

import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize
import random
import poetrytools
import os

class Poem:
	"""	Class: Poem
		Description: scores, analyzes for tone, and print sonnets (which are lists of word objects)
		Parameters: 
			sonnet --> created poem
		Methods:
			get_str --> puts lists of word objects into printable string
			get_raw_str --> puts sonnet together in one string without breaks or capitalization for analysis
			get_score --> scores sonnet based on how good its rhymes, syllables, and meter are
			get_tone --> analyzes sonnet for net positive, negative, or neutral tone
	"""
	def __init__(self, sonnet):
		self.sonnet = sonnet

	def __str__(self):
		str_rep = self.get_str()
		return str_rep

	def get_str(self):
		str_rep = ""
		for line in self.sonnet:
			for word in line:
				if word == line[0]:
					str_rep += word.name.capitalize() + " "
				elif word == line[len(line)-1]:
					str_rep += word.name + ",\n"
				else:
					str_rep += word.name + " "
		str_rep = str_rep[:-2]
		str_rep += ".\n"
		return str_rep

	def get_raw_str(self):
		str_rep = ""
		for line in self.sonnet:
			for word in line:
				if word == line[len(line)-1]:
					str_rep += word.name + ","
				else:
					str_rep += word.name + " "

		count = str_rep.count("\'")
		if count%2 != 0:
			str_rep += "\'"

		return str_rep

	def get_score(self):
		score = 0

		# score rhymes
		rhyme_score = 0
		rhyme_check = [0, 1, 4, 5, 8, 9]
		last_word_list = []

		# get words at end of each line to check
		for line in self.sonnet:
			last_word = line[len(line)-1].name
			last_word_list.append(last_word)

		# check for ababcdcdefefgg rhyme scheme and add to score for each good rhyme
		for word in rhyme_check:
			if poetrytools.rhymes(last_word_list[word],last_word_list[word+2]):
				rhyme_score += 1
		if poetrytools.rhymes(last_word_list[12],last_word_list[13]):
			rhyme_score += 1

		# score syllables
		syllable_score = 0
		for line in self.sonnet:
			syllable_count = 0
			for word in line:
				syllable_count += word.get_syllables()
			syllable_score -= abs(10-syllable_count)

		#score meter
		meter_score = 0
		str_rep = self.get_str()
		poem = poetrytools.tokenize(str_rep)
		meter = poetrytools.scanscion(poem)
		for line in meter:
			for word in line:
				if word == "01":
					meter_score += 1

		score += rhyme_score + syllable_score + meter_score
		scores = [score, rhyme_score, 140-abs(syllable_score), meter_score]

		return scores

	def get_tone(self, positives, negatives):
		tone = 0
		for word in self.get_raw_str().split():
			if word in positives:
				tone += 1
			if word in negatives:
				tone -= 1
		return tone

class Word:
	"""	Class: Word
		Description: words from the original sonnets
		Parameters: 
			name --> the actual word
		Methods:
			get_syllables --> get how many syllables in word
			get_speech --> get part of speech of word
	"""
	def __init__(self, name):
		self.name = name

	def __str__(self):
		str_rep = self.name + " : " + str(self.get_speech()) + " : "
		str_rep += str(self.syllables) + " syllables"
		return str_rep

	def get_syllables(self):
		# get number of syllables based on vowel placement
		syllables = 0
		vowels = "aeiou"
		word = self.name.lower()
		if word[0] in vowels:
			syllables += 1
		for i in range(1, len(word)):
			if word[i] in vowels and word[i-1] not in vowels and word[i-1] != 'y':
				syllables += 1
		if word[-1] == 'e':
			syllables -= 1
		if word[-1] == 'le':
			syllables += 1
		if syllables == 0:
			syllables += 1
		return syllables

	def get_speech(self):
		# get part of speech of word from nltk
		text = word_tokenize(self.name)
		speech = nltk.pos_tag(text)
		return speech[0][1]

def read_in_sonnets():
	# create word objects for each word in inspiring set of sonnets

	end_chars = ".,:;?!'"

	f = open('sonnets.txt','r')
	words = []
	lines = f.readlines()
	for i in range(len(lines)):
		for j in range(len(lines[i].split())):
			line = lines[i].split()
			if line[j][-1] in end_chars:
				full_word = line[j].lower()
				word = Word(full_word[:-1])
			else:
				word = Word(line[j].lower())
			words.append(word)
	f.close()
	return words

def read_in_positives():
	# read in list of positive tone words
	f = open('positives.txt', 'r')
	positives = f.read().splitlines()
	lines = f.readlines()
	f.close()
	return positives

def read_in_negatives():
	# read in list of negative tone words 
	f = open('negatives.txt', 'r')
	negatives = f.read().splitlines()
	lines = f.readlines()
	f.close()
	return negatives

def create_sonnet(sonnets):

	# start with random word for part of speech
	word_pos = random.randint(0, len(sonnets)-1)
	speech = sonnets[word_pos].get_speech()

	lines = []
	line_number = 0
	last_word_list = []

	# for each of 14 lines, add words in part of speech order until line hits 10 syllables
	for i in range(14):
		line = []
		syllable_count = 0
		count = 0

		# keep adding words until the line is at 10 syllables
		while syllable_count != 10:
			word_index = random.randint(0, len(sonnets)-1)
			word = sonnets[word_index]

			# new word must be the correct part of speech based on inspiring set
			while word.get_speech() != speech:
				word_index = random.randint(0, len(sonnets)-1)
				word = sonnets[word_index]	

			# if reach the end of inspiring set, start again
			word_pos += 1
			if word_pos == 17517:
				word_pos = 0
			speech = speech = sonnets[word_pos].get_speech()

			# if word is right part of speech and within syllable range, add it
			if word.get_syllables() <= (10 - syllable_count):
				line.append(word)
				syllable_count += word.get_syllables()

		# for lines that rhyme, look for a rhyming word to match end of each line
		if (i > 1 and i < 4) or (i > 5 and i < 8) or (i > 9 and i < 12) or (i == 13):
			if i == 13:
				rhyme_pair = 1
			else:
				rhyme_pair = 2
			prev_rhyme = last_word_list[i-rhyme_pair]
			last_word = line.pop(len(line)-1)
			count = 0

			# look for rhyming words with word at end of line
			while not poetrytools.rhymes(prev_rhyme.name, last_word.name) and count < 10000:
				word_index = random.randint(0, len(sonnets)-1)
				last_word = sonnets[word_index]
				count += 1

			# add line to list of lines
			line.append(last_word)

		last_word_list.append(line[len(line)-1])
		lines.append(line)
		line_number += 1

	return lines

def main():

	# read in inspiring set and inspiring tones
	sonnets = read_in_sonnets()
	positives = read_in_positives()
	negatives = read_in_negatives()

	# create a certain number of sonnets to compare
	sonnet_list = []
	for i in range(10):
		sonnet = Poem(create_sonnet(sonnets))
		sonnet_list.append(sonnet)

	# score each sonnet and find the best one
	highest_score = [0]
	best_sonnet = ""
	for sonnet in sonnet_list:
		score = sonnet.get_score()
		total_score = score[0]
		if total_score > highest_score[0]:
			highest_score = score
			best_sonnet = sonnet

	# print the best sonnet
	print("\nSONNET CLV")
	print(best_sonnet)

	# print the score of the best sonnet
	#print("Total Score: " + str(highest_score[0]))
	print("Rhyme Score: " + str(round(highest_score[1]/7*100)) + "%")
	print("Syllable Score: " + str(round(highest_score[2]/140*100)) + "%")
	print("Meter Score: " + str(round(highest_score[3]/70*100)) + "%\n")

	# get tone of best sonnet and read it depending on the tone
	tone = best_sonnet.get_tone(positives, negatives) 

	if tone > 0:
		os.system("say -v Vicki " + (best_sonnet.get_raw_str()))
	elif tone < 0:
		os.system("say -v Bad News " + (best_sonnet.get_raw_str()))
	elif tone == 0:
		os.system("say -v Samantha " + (best_sonnet.get_raw_str()))


main()
