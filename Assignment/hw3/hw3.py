import numpy as np 

def prob(alpha,B_integer,z):
	t = abs(z - B_integer)
	return (1 - alpha) / (1 + alpha) * (alpha ** t)

# N_list = [i for i in range(100,1001,10)]
N_list = [100000]
result_list = []
count = 0
for N in N_list:
	numerator,denominator = 0,0
	for i in range(N):
		B = np.random.choice([0,1],size = 10, p = [.5,.5])
		B_integer = int("".join(str(x) for x in B),2)
		probability = prob(0.1,B_integer,128)
		numerator += B[1] * probability
		denominator += probability
		print(B[1],probability)
	result = numerator / denominator
	result_list.append(result)
print(result_list)

