# Joseph Shaffer
# CSE 5243 Programming Assignment 2


import random
import time
import math

i = 0
dict = {}
overall = {}
positive = {}
negative = {}
sentiments = []
trainSet = []
testSet =[]
validSet = []
accuracies = {}

with open('amazon_cells_labelled.txt', 'r') as file:
	for line in file:
		dict1 = {}	
		l = line.split()
		sentiment = l[-1]
		sentiments.append(sentiment)
		del l[-1]
		for word in l:
			if overall.has_key(word):
				overall[word] = overall[word] + 1
			else:
				overall[word] = 1
			if dict1.has_key(word):
				dict1[word] = dict1[word] + 1
			else:
				dict1[word] = 1
			if sentiment == '1':
				if positive.has_key(word):
					positive[word] = positive[word] + 1
				else:
					positive[word] = 1
			else:
				if negative.has_key(word):
					negative[word] = negative[word] + 1
				else:
					negative[word] =1
		dict[i] = dict1
		i = i + 1	

with open('imdb_labelled.txt', 'r') as file:
	for line in file:
		dict1 = {}
		l = line.split()
		sentiment = l[-1]
		sentiments.append(sentiment)
		del l[-1]
		for word in l:
			if overall.has_key(word):
				overall[word] = overall[word] + 1
			else:
				overall[word] = 1
			if dict1.has_key(word):
				dict1[word] = dict1[word] + 1
			else:
				dict1[word] = 1
			if sentiment == '1':
				if positive.has_key(word):
					positive[word] = positive[word] + 1
				else:
					positive[word] = 1
			else:
				if negative.has_key(word):
					negative[word] = negative[word] + 1
				else:
					negative[word] =1
		dict[i] = dict1
		i = i + 1	

with open('yelp_labelled.txt', 'r') as file:
	for line in file:
		dict1 = {}
		l = line.split()
		sentiment = l[-1]
		sentiments.append(sentiment)
		del l[-1]
		for word in l:
			if overall.has_key(word):
				overall[word] = overall[word] + 1
			else:
				overall[word] = 1
			if dict1.has_key(word):
				dict1[word] = dict1[word] + 1
			else:
				dict1[word] = 1
			if sentiment == '1':
				if positive.has_key(word):
					positive[word] = positive[word] + 1
				else:
					positive[word] = 1
			else:
				if negative.has_key(word):
					negative[word] = negative[word] + 1
				else:
					negative[word] =1
		dict[i] = dict1
		i = i + 1
	
def rand(k):
	index = range(3000)
	random.shuffle(index)
	end = int((k / 100.0) * 3000)
	for x in range(0, end):
		trainSet.append(index[x])
	end2 = (3000 - end) / 2 + end
	for x in range(end, end2):
		validSet.append(index[x])
	for x in range(end2, 3000):
		testSet.append(index[x])

def knn(k, dataSet):
	correctPred = 0
	totalPred = len(dataSet) * 1.0
	for x in dataSet:
		similarities = {}
		neighbors = []
	#print x
		for y in trainSet:
		#print y
			if x != y:
				similar = 0
				for word in dict[y].keys():
					if dict[x].has_key(word):
						similar = similar + 1
				similarities[y] = similar
	#print similarities
		for z in range(0, k):
			neighbor = mostSimilar(similarities)
			neighbors.append(neighbor)
			if neighbor != 0:
				del similarities[neighbor]
		predict = prediction(neighbors)
		if sentiments[x] == predict:
			correctPred = correctPred + 1
	accuracy = correctPred / totalPred
	return accuracy

def mostSimilar(a):
	maxSim = 0
	neighbor = 0
	for x in a.keys():
		if a[x] > maxSim:
			maxSim = a[x]
			neighbor = x
	#print neighbor
	return neighbor	

#print len(sentiments)

def prediction(a):
	ones = 0
	zeros = 0
	for x in a:
		#print sentiments[x]
		if sentiments[x] == '1':
			ones = ones + 1
		else: 
			zeros = zeros + 1
	if ones > zeros:
		return '1'
	else: 
		return '0'

def findOptK():
	maxAcc = 0.0
	optK = 0
	for x in accuracies.keys():
		if accuracies[x] > maxAcc:
			maxAcc = accuracies[x]
			optK = x
	return optK

def pruning(k, threshold):
	frequentWords = []
	deleted = []
	for x in dict.keys():
		for y in dict[x].keys():
			if positive.has_key(y) and negative.has_key(y):
				if math.fabs(positive[y] - negative[y])/overall[y] <= threshold:
					del dict[x][y]
					if y not in deleted:
						deleted.append(y)
	for x in deleted:
		if overall.has_key(x):
			del overall[x]
	for x in range(0, k):
		word = mostFrequentWord()
		frequentWords.append(word)
		del overall[word]
	for x in dict.keys():
		for y in dict[x].keys():
			if not any(z == y for z in frequentWords):
				del dict[x][y]
	

def mostFrequentWord():
	count = 0
	word = ""
	for x in overall.keys():
		if overall[x] > count:
			count = overall[x]
			word = x
	return word
	
def bayes(dataSet):
	correctPred = 0
	totalPred = len(dataSet)
	positive = 0
	negative = 0
	for x in trainSet:
		if sentiments[x] == '1':
			positive += 1
		else:
			negative += 1
	posProb = (positive * 1.0) / len(trainSet)
	negProb = (negative * 1.0) / len(trainSet)
	for x in dataSet:
		posProbabilities = []
		negProbabilities = []
		for y in dict[x].keys():
			probs = []
			probs.append(0)
			probs.append(0)
			for z in trainSet:
				if dict[z].has_key(y):
					if sentiments[z] == '1':
						probs[1] += 1
					else:
						probs[0] += 1
			posProbabilities.append((probs[1] * 1.0 + 1.0) / (positive + 1))
			negProbabilities.append((probs[0] * 1.0 + 1.0) / (negative + 1))
		total = 1
		for t in range(0, len(posProbabilities)):
			#print "Positive Probabilities %f" %(posProbabilities[t])
			total *= (posProbabilities[t] * 100)
		#print total
		positiveProb = posProb * total
		#print "Positive Probability: %f" %(positiveProb)
		total = 1
		for t in range(0, len(negProbabilities)):
			#print "Negative Probabilities %f" %(negProbabilities[t])
			total *= (negProbabilities[t] * 100)
		negativeProb = negProb * total
		#print "Negative Probability: %f" %(negativeProb)
		predict = ""
		if positiveProb >= negativeProb:
			predict = '1'
		else:
			predict = '0'
		#print "Prediction: %s" %(predict)
		#print "Actual: %s" %(sentiments[x])
		if sentiments[x] == predict:
			correctPred += 1
	accuracy = correctPred * 1.0 / totalPred
	#print "Accuracy is: %f" %(accuracy)
	return accuracy


def main():
	k = [1, 3, 5, 7]
	rand(60)	
	
	print "\nTraining set is 60% of data \n"
	
	print "Test set is 20% of data \n"

	print "Valid set is 20% of data \n"

	print "Original Feature Vector: \n"	
	
	print "KNN Classifier \n"

	for x in k:
		accuracies[x] = knn(x, validSet)
	optimalK = findOptK()
	#print optimalK

	print "From Training and Validation Set: Optimal Value of K: %d \n" %(optimalK)
	
	acc = knn(optimalK, trainSet)
	print "Training Set: The accuracy is %.2f percent \n" %(acc * 100.0)

	print "Validation Set: The accuracy is %.2f percent \n" %(accuracies[optimalK] * 100.0)

	t1 = time.time()
	acc = knn(optimalK, testSet)
	t2 = time.time()
	timePerTuple = (t2-t1) / len(testSet)

	print "Test Set: The accuracy is %.2f percent \n" %(acc * 100.0)
	print "Test Set: The time to classify per tuple is %f seconds \n" %(timePerTuple)

	acc = bayes(trainSet)
	
	print "Naive Bayes Classifier: \n"
	
	print "Training Set: The accuracy is %.2f percent \n" %(acc)
	
	acc = bayes(validSet)

	print "Validation Set: The accuracy is %.2f percent \n" %(acc)

	t1 =time.time()
	acc = bayes(testSet)
	t2 = time.time()
	timePerTuple = (t2-t1) / len(testSet)

	print "Test Set: The accuracy is %.2f percent \n" %(acc)
	print "Test Set: The time to classify per tuple is %f seconds \n" %(timePerTuple)

	pruning(1000, 0.4)

	print "Pruned Feature Vector: \n"

	for x in k:
		accuracies[x] = knn(x, validSet)
	optimalK = findOptK()
	#print optimalK
	print "KNN Classifier: \n"

	print "From Training Set and Validation Set: Optimal Value of K: %d \n" %(optimalK)
	
	acc = knn(optimalK, trainSet)
	print "Training Set: The accuracy is %.2f percent \n" %(acc * 100.0)

	print "Validation Set: The accuracy is %.2f percent \n" %(accuracies[optimalK] * 100.0)

	t1 = time.time()
	acc = knn(optimalK, testSet)
	t2 = time.time()
	timePerTuple = (t2-t1) / len(testSet)

	print "Test Set: The accuracy is %.2f percent \n" %(acc * 100.0)
	print "Test Set: Time to classify per tuple is %f seconds \n" %(timePerTuple)

	acc = bayes(trainSet)
	
	print "Naive Bayes Classifier \n"

	print "Training Set: The accuracy is %.2f percent \n" %(acc)
	
	acc = bayes(validSet)

	print "Validation Set: The accuracy is %.2f percent \n" %(acc)

	t1 =time.time()
	acc = bayes(testSet)
	t2 = time.time()
	timePerTuple = (t2-t1) / len(testSet)

	print "Test Set: The accuracy is %.2f percent \n" %(acc)
	print "Test Set: The time to classify per tuple is %f seconds \n" %(timePerTuple)

main()


