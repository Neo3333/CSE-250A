import numpy as np
import time 


time1 = time.time()
with open("hw1_word_counts_05.txt", 'r') as f:
	contents = f.readlines()

n = 5

words = []
nums = []
prior = {}
for item in contents:
	word, num = item.split()
	if len(word) == 5:
		words.append(word)
		nums.append(int(num))

words = np.array(words)
nums = np.array(nums)
total_words = np.sum(nums)

for i, count in enumerate(nums):
	prob = (count + 0.0) / total_words
	prior[words[i]] = prob

# Sanity Check
#print(words[np.argmax(nums)])
#print(words[np.argmin(nums)])


def compute_marginal(word, next_charac, position):
	flag = False
	for i in position:
		if word[i - 1] == next_charac: flag = True
	if flag: 
		return 1
	else: return 0

def compute_denominator(true_charac, true_positions, false_charac):
	false_positions = [item for item in [1,2,3,4,5] if item not in true_positions]
	# compute denominator
	denominator = 0
	for w in words:
		flag1 = True
		flag2 = False
		for i, charac in enumerate(true_charac):
			if w[true_positions[i] - 1] != charac: flag1 = False
		for i in false_positions:
			if (w[i - 1] in false_charac) or (w[i - 1] in true_charac): flag2 = True
		if flag1 and flag2 == False: 
			denominator += prior[w]
	return denominator

def compute_Bayes(word, true_charac, true_positions, false_charac, denominator):
	false_positions = [item for item in [1,2,3,4,5] if item not in true_positions]

	# compute numerator
	flag1 = True
	flag2 = False
	for i, charac in enumerate(true_charac):
		if word[true_positions[i] - 1] != charac: flag1 = False
	for i in false_positions:
		if (word[i - 1] in false_charac) or (word[i - 1] in true_charac): flag2 = True
	#for i, charac in enumerate(false_charac):
	#	for j in false_positions:
	#		if word[j - 1] == charac: flag2 = True
	if flag1 and flag2 == False: numerator = prior[word]
	else: numerator = 0
	return numerator / denominator


def compute_prediction(next_charac, true_charac, true_positions, false_charac):
	prob = 0
	denominator = compute_denominator(true_charac, true_positions, false_charac)
	for word in words:
		marginal = compute_marginal(word, next_charac, [item for item in [1,2,3,4,5] if item not in true_positions])
		if marginal != 0:
			bayes = compute_Bayes(word, true_charac, true_positions, false_charac, denominator)
			prob += bayes * marginal
	return prob



# Begin hangman initialization
#TEST CASE 1:
arg1 = [[], [], ["A", "S"], ["A", "S"], ["O"], [], ["D", "I"], ["D", "I"], ["U"]]
arg2 = [[],[], [1, 5], [1, 5], [3], [], [1, 4], [1, 4], [2]]
arg3 = [[], ["E", "A"], [], ["I"], ["A", "E", "M", "N", "T"], ["E", "O"], [], ["A"], ["A", "E", "I", "O", "S"]]
alphabetic = list(map(chr, range(65, 91)))
for i in range(len(arg1)):
	true_charac, true_positions, false_charac = arg1[i], arg2[i], arg3[i]
	max = 0
	next_guess = ""
	for char in [item for item in alphabetic if item not in true_charac and item not in false_charac]:
		prob = compute_prediction(char, true_charac, true_positions, false_charac)
		if prob > max:
			max = prob
			next_guess = char
	print("The next best guess is ", next_guess, "with probability ", max)


print(time.time() - time1)