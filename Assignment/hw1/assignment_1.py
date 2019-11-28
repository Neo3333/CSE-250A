import numpy as np
import time

class Hangman(object):

	# correct prior: numpy array with length 5 [a1,a2,a3,a4,a5],each represents a letter index, -1 means undecided;
	# for the letter index, A = 1, B = 2, ..., Z = 26;
	# incorrect prior: numpy array containing index of letters that doesn't appear in the word;

	def __init__(self,correct_prior,incorrect_prior):
		self.correct = correct_prior
		self.incorrect = incorrect_prior

	def prob_1(self,word_list_numerical):
		mask = []
		result = np.zeros((26,len(word_list_numerical)))
		for item in self.incorrect:
			result[item] = 0
		for item in self.correct:
			if item == -1:
				mask.append(1)
			else:
				mask.append(0)
		mask = np.array(mask)
		word_list_mask = word_list_numerical * mask
		for i in range(len(word_list_mask)):
			for j in range(5):
				index = word_list_mask[i][j]
				if index != 0:
					result[index-1][i] = 1
		return result

	def prob_2(self,word_list_numerical,percent):
	
		temp = list(set(self.correct))
		temp.remove(-1)
		result = np.zeros(len(word_list_numerical))
		for i in range(len(word_list_numerical)):
			flag = 0
			for item in self.incorrect:
				if item in word_list_numerical[i]:
					flag = 1
					break
			if flag == 1:
				continue
			for j in range(len(self.correct)):
				if self.correct[j] != word_list_numerical[i][j] and self.correct[j] != -1:
					flag = 1
					break
				if self.correct[j] == -1 and word_list_numerical[i][j] in temp:
					flag = 1
					break
			if flag == 1:
				continue
			result[i] = 1
		result_percent = result * percent
		result2 = np.sum(result_percent)
		return result,result2

if __name__ == "__main__":
	time_start = time.time()
	
	#read the file
	with open("hw1_word_counts_05.txt","r") as f:
		contents = f.readlines()

	word_list,count_list = [],[]

	for word_count in contents:
		word,count = word_count.split()
		if len(word) == 5:
			word_list.append(word)
			count_list.append(int(count))

	np_count_list = np.array(count_list)
	result = np.argsort(np_count_list)
	total = np.sum(np_count_list)
	percent = np_count_list / total

	#most and least frequent words
	most_15 = result[len(result) - 15:]
	least_14 = result[:14]
	print("Most 15 frequent words ",end = '')
	for item in most_15:
		print(word_list[item],end = ' ')
	print()
	print("Least 14 frequent words ",end = '')
	for item in least_14:
		print(word_list[item],end = ' ')
	print()
	#transfer each word in the word_list to integers
	q = []
	for item in word_list:
		q.append([ord(c) for c in item])
	word_list_numerical = np.array(q)
	word_list_numerical -= 64

	#initialization
	correct_prior_list = np.array([[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1],[1,-1,-1,-1,19],[1,-1,-1,-1,19],[-1,-1,15,-1,-1],
		[-1,-1,-1,-1,-1],[4,-1,-1,9,-1],[4,-1,-1,9,-1],[-1,21,-1,-1,-1]])
	incorrect_prior_list = np.array([[],[1,5],[],[9],[1,5,13,14,20],[5,15],[],[1],[1,5,9,15,19]])
	for i in range(len(correct_prior_list)):
		h = Hangman(correct_prior_list[i],incorrect_prior_list[i])
		p1 = h.prob_1(word_list_numerical)
		p2,p2_percent = h.prob_2(word_list_numerical,percent)
		p3 = p2 * percent / p2_percent * p1
		p3 = np.sum(p3,axis = 1)
		index = np.where(p3 == np.max(p3))
		print("Next best guess is " + chr(index[0][0]+65)+" the probability of the guess is " + str(max(p3)))
	time_end = time.time()
	print('total_cost',time_end - time_start)

