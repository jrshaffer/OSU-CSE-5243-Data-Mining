# Joseph Shaffer
# CSE 5243 Programming Assignment 1


int = 1
dict = {}

with open('amazon_cells_labelled.txt', 'r') as file:
	for line in file:
		dict1 = {}
		for word in line.split():
			if dict1.has_key(word):
				dict1[word] = dict1[word] + 1
			else:
				dict1[word] = 1
		dict[int] = dict1
		int = int + 1	

with open('imdb_labelled.txt', 'r') as file:
	for line in file:
		dict1 = {}
		for word in line.split():
			if dict1.has_key(word):
				dict1[word] = dict1[word] + 1
			else:
				dict1[word] = 1
		dict[int] = dict1
		int = int + 1	

with open('yelp_labelled.txt', 'r') as file:
	for line in file:
		dict1 = {}
		for word in line.split():
			if dict1.has_key(word):
				dict1[word] = dict1[word] + 1
			else:
				dict1[word] = 1
		dict[int] = dict1
		int = int + 1

for x in range(500, 3500, 500):
	print "Sentence %d:" %(x)
	for y in dict[x].keys():
		print "Word: '%s', Count: %s" %(y, dict [x] [y])


