# Joseph Shaffer
# CSE 5243 Programming Assignment 3


import random
import time
import math

sentences = []
words = set()
similarities = []
#minhash = []
documentMatrix = []
docMatrixSim = []


with open('amazon_cells_labelled.txt', 'r') as file:
	for line in file:
		sentence = set()	
		l = line.split()
		del l[-1]
		for word in l:
			sentence.add(word.lower())
		sentences.append(sentence)
		words = words.union(sentence)
	

with open('imdb_labelled.txt', 'r') as file:
	for line in file:
		sentence = set()	
		l = line.split()
		del l[-1]
		for word in l:
			sentence.add(word.lower())
		sentences.append(sentence)
		words = words.union(sentence)	

with open('yelp_labelled.txt', 'r') as file:
	for line in file:
		sentence = set()	
		l = line.split()
		del l[-1]
		for word in l:
			sentence.add(word.lower())
		sentences.append(sentence)
		words = words.union(sentence)
	
def jaccard():
	index = 0
	comparisons = 0
	for x in sentences:
		sims = []
		index2 = 0
		for y in sentences:
			if index2 > index:
				similarity = len(x.intersection(y))/float(len(x.union(y)))
				#print "Similarity: %.6f" %(similarity)
				comparisons += 1
				sims.append(similarity)
			index2 += 1
		if sims:
			similarities.append(sims)
		#if index == 0:
			#print(sims)
			#print(similarities)
		index += 1
	return comparisons
	#print(count)

def createDocumentMatrix():
	for x in words:
		row = []
		for y in sentences:
			if x in y:
				row.append(1)
			else:
				row.append(0)
		documentMatrix.append(row)

def kminhash(k):
	sigMatrix = []
	#print(len(sentences))
	indices = range(len(words))
	#print(indices)
	for x in range(0, k):
		sig = []
		random.shuffle(indices)
		for y in range(0, 3000):
			sig.append(findMatrixValue(indices, 0, y))
		sigMatrix.append(sig)	
	return sigMatrix
	
def findMatrixValue(indices, count, column):
	row = indices[count]
	while documentMatrix[row][column] != 1:
		count += 1
		row = indices[count]
	return row + 1

def minhashSimilarity(sigMatrix, k):
	#counter = 0
	minhash = []
	for x in range(0, 2999):
		sim = []
		column = x + 1
		while column < 3000:
			count = 0
			for y in range(0, k):
				if sigMatrix[y][x] == sigMatrix[y][column]:
					count += 1			
			sim.append(count/float(k))
			column += 1
		minhash.append(sim)
	return minhash

def matrixSimilarities():
	for x in range(0, 2):
		sim = []
		column = x + 1
		while column < 3000:
			count = 0
			total = 0
			for y in range(0, len(words)):
				if documentMatrix[y][x] == 1 or documentMatrix[y][column] == 1:
					total += 1
					if documentMatrix[y][x] == documentMatrix[y][column]:
						count += 1
			sim.append(count/float(len(words)))
			column += 1
		docMatrixSim.append(sim)
		

def meanError(minhash):
	error = 0
	totalError = 0
	#print(len(minhash))
	for x in range(0, len(similarities)):
		for y in range(0, len(similarities[x])):
			error = math.pow(similarities[x][y] - minhash[x][y], 2)
			totalError += error
	return totalError		
	

def main():
	k = [16, 32, 64, 128, 256]
	t1 = time.time()
	comparisons = jaccard()
	t2 = time.time() - t1
	print "Time to find Similarity between 2 sentences with Intersection of those 2 Sentences divided by Union of those 2 Sentences: %f seconds" %(t2 / float(comparisons))
	createDocumentMatrix()
	t3 = time.time()
	matrixSimilarities()
	t4 = time.time() - t3
	print "Time to find Similarity with Jaccard Similarity from Document Matrix between 2 sentences: %f seconds" %(t4 / float(2999 + 2998))
	for x in k:
		sigMatrix = kminhash(x)
		t5 = time.time()
		minhash = minhashSimilarity(sigMatrix, x)
		t6 = time.time()-t5
		print "Time to find Similarity Estimate from Signature Matrix between 2 Sentences with K = %d: %f seconds" %(x, t6 / float(comparisons))
		totalError = meanError(minhash)
		print "Mean Square Error between Baseline Similarity and Similarity Estimate with K = %d: %f" %(x, totalError/ float(comparisons))

main()


