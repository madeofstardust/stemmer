##This is my stemmer.
##stemmer looks for stems in a words given by the user
##First input some words / a sentence
##

# Importing the libraries
import pandas as pd
import re

# Importing datasets:
dataset_verbs = pd.read_csv('pronouns.csv')
X_p = dataset_verbs.iloc[:, 0].values

dataset_verbs = pd.read_csv('verbsbe.csv')
X_vb = dataset_verbs.iloc[:, 0].values

dataset_verbs = pd.read_csv('prepositions.csv')
X_pre = dataset_verbs.iloc[:, 0].values

dataset_verbs = pd.read_csv('irregular.csv')
X_v = dataset_verbs.iloc[:, [1, 2] ].values
Y_v = dataset_verbs.iloc[:, 0].values

dataset_adj = pd.read_csv('adjectives.csv')
X_a = dataset_adj.iloc[:, [1, 2] ].values
Y_a = dataset_adj.iloc[:, 0].values

# no., of steps:
steps = 0;

# input a sentence of Your choice:
y = input("input the sentence of Your choice: \n")
y = y.split()
l = []

# Two additional counters:
pn = 0

pa = 0

# Functions:
# Looking for and removing eventual punctuation marks:


def if_punctuation(word):
	if re.match(".+[.,?!-%()]", word):
		word = re.sub("[.,?!-%()]", "", word)
	return word


def if_article(word):
	if word == "a" or word == "the":
		print("Your word:", word, "lemma:", word, ", part of speech: article.")
		# if yes, then, if everything else fails in the case of the word following this one, we can assume that it
		# will be a noun
		global pn
		pn = 1
		return 1


def if_irregular_verb(word):
	for i in range(0, 138):
		z = X_v[i,0]
		v = X_v[i, 1]
		vv = Y_v[i]
		if word == z or word == v or word == vv:
			print("Your word:", word,"lemma:", vv, ", part of speech: verb.")
			print("Number os steps: 1")
			return 1


def if_irregular_adjective(word):
	for i in range(0, 4):
		z = X_a[i,0]
		v = X_a[i, 1]
		if word == z or word == v:
			y = Y_a[i]
			print("Your word: ", word,"lemma:", y, ", part of speech: adjective.")
			print("Number os steps: 1")
			return(1)


def if_pronoun(word):
	for i in range(0, 83):
		z = X_p[i]
		if word == z:
			print("Your word: ", word,"lemma:", z, ", part of speech: pronoun.")
			print("Number os steps: 1")
			return(1)


def if_preposition(word):
	for i in range(0, 45):
		z = X_pre[i]
		if word == z:
			print("Your word: ", word,"lemma:", z, ", part of speech: preposition.")
			print("Number os steps: 1")
			return(1)


def if_be(word):
	for i in range(0, 4):
		z = X_vb[i]
		if word == z:
			print("Your word: ", x,"lemma: be, part of speech: verb.")
			print("Number os steps: 1")
			# if other things fail for the next word, then it probably is an adjective:
			global pa
			pa = 1
			return 1

# Everything to lowercase:
for i in y:
	l.append(i.lower())

# The main loop:

for x in l:
	# look for punctuation marks and removing them:
	x = if_punctuation(x)

	# Articles are pretty common, and therefore we first look for such:
	# check if a or the
	if if_article(x):
		continue

	# First, i check for different irregularities that there can be; a stemmer generally can have problems with
	# irregular adjectives, verbs etc, and therefore the given below function first check for such, and assign their
	# stems from the list

	# check if it is an irregular verb:
	if if_irregular_verb(x):
		continue
	
	# check if it is an irregular adjective:
	if if_irregular_adjective(x):
		continue

	# check if be:
	if if_be(x):
		continue

	# Pronouns and prepositions are hard to classify, and therefore I use the same method as before:
	# check if pronoun:
	if if_pronoun(x):
		continue
		
	# check if preposition:
	if if_preposition(x):
		continue

	# Now, the proper part: looking for pre- and suffixes:
	# endings:
	if re.search("(sses)$", x):
		y = re.sub("(sses)$", "ss", x)
		p = "noun"
		steps = steps + 1
	elif re.search("(ies)$", x):
		y = re.sub("(ies)$", "y", x)
		steps = steps + 1
		p = "noun or verb"
	elif re.search(".+([aeiou])(ves)$",x):
		y = re.sub("(ves)$", "fe", x)
		steps = steps + 1
		p = "noun"
	elif re.search(".+([^aeiou])(ves)$",x):
		y = re.sub("(ves)$", "f", x)
		steps = steps + 1
		p = "noun"	
	elif re.search("(s)$", x):
		y = re.sub("(s)$", "", x)
		steps = steps + 1
		p = "noun or verb"	
	elif re.search("((([aeiou])([^aeiou]))(ed))$", x):
		y = re.sub("(ed)$", "", x)
		steps = steps + 1
		p ="verb"
	elif re.search("((([aeiou])([^aeiou]))+(.+)(ed))$", x):
		y = re.sub("(ed)$", "e", x)
		steps = steps + 1
		p ="verb"
	elif re.search("(n't)$",x):
		y = re.sub("(n't)$", " not", x)
		steps = steps+1
		p = "verb"
	elif re.search("((([aeiou])([^aeiou])*)(ing))$", x):
		y = re.sub("(ing)$", "", x)
		steps = steps + 1
		p ="verb"
	elif re.search("((([aeiou])([^aeiou]))(ational))$", x):
		y = re.sub("(ational)$", "ate", x)
		steps = steps + 1
		p = "adjective"
	elif re.search("((([^aeiou])([aeiou]))(tional))$", x):
		y = re.sub("(tional)$", "tion", x)
		steps = steps + 1
		p = "adjective"
	elif re.search("(([aeiou])([^aeiou])*([aeiou])([^aeiou])(ance))$", x):
		y = re.sub("(ance)$", "", x)
		steps = steps + 1
		p = "noun"
	elif re.search("(([aeiou])([^aeiou])*([aeiou])([^aeiou])(ence))$", x):
		y = re.sub("(ence)$", "", x)
		steps = steps + 1
		p = "noun"
	elif re.search("(([aeiou])([^aeiou])*([aeiou])([^aeiou])(ly))$", x)	:
		steps = steps + 1
		y = x
		p = "adjective"
	#beginnings:
	elif re.search("^(re).+",x):
		steps = steps+1
		y = re.sub("^(re)", "", x)
		p = "verb"
	elif re.search("^(sub).+",x):
		steps = steps+1
		y = re.sub("^(sub)", "", x)
		print (y)
		p = "noun"	
	elif re.search("^(un).+",x):
		steps = steps+1
		y = re.sub("^(un)", "", x)
		p = "verb"	
	elif re.search("^(de).+",x):
		steps = steps+1
		y = re.sub("^(de)", "", x)
		p = "verb"	
	elif re.search("^(hetero).+",x):
		steps = steps+1
		y = re.sub("^(hetero)", "", x)
		p = "adjective"
	elif re.search("^(homo.+)",x):
		steps = steps+1
		y = re.sub("^(homo)", "", x)
		p = "adjective"		
	elif re.search("^(hyper).+",x):
		steps = steps+1
		y = re.sub("^(hyper)", "", x)
		p = "adjective"		
	elif re.search("^(macro).+",x):
		steps = steps+1
		y = re.sub("^(macro)", "", x)
		p = "noun"	
	elif re.search("^(micro)",x):
		steps = steps+1
		y = re.sub("^(micro).+", "", x)
		p = "noun"	
	elif re.search("^(mono)",x):
		steps = steps+1
		y = x
		p = "noun"		
	else:
		y = x
		p = "probably noun"

	#last chance:
	if pn == 1:
		steps = steps+1
		y = x;
		p = "noun"
		pn = 0
	elif pa == 1:
		steps = steps +1
		y = x;
		p = "adjective"
		pa = 0
		
	print("Your word: ", x,"lemma:", y, ", part of speech:", p)
	print("Number os steps:", steps)