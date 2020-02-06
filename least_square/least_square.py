import numpy as np
import json




#================================================================================
# kernel function 
def c_func(x):
	return 1
def x_func(x):
	return x

def x2_func(x):
	return x**2
def x3_func(x):
	return x**3

#=================================================================================

# 基底
def basis(x):
	return np.array([c_func(x),x_func(x),x2_func(x),x3_func(x)]).reshape(-1,1)


def model(w,x):
	return (np.transpose(w)@ basis(x)).item()



if __name__ == '__main__':
	with open("../data/2019_nCoV.json",encoding='utf8') as f: 
		j = json.load(f)
	xdata = j['x']
	ydata = j['y']

	# compute A-inverse 
	n = len(xdata)
	A = np.zeros((4,4))
	b = np.zeros((4,1))
	for i in range(n):
		phi = basis(xdata[i])
		phiT = np.transpose(phi)
		A+= phi @ phiT
		b += ydata[i]*phi
	invA = np.linalg.inv(A)	
	# compute w
	w = (invA @ b).reshape(-1)
	
	# compute r2 
	res = 0.0
	mu = np.mean(ydata)
	tot = 0.0
	for i in range(n):
		res += (ydata[i] - model(w,xdata[i]))**2
		tot += (ydata[i] - mu)**2
	r2 = 1-res/tot

	print("w:{}".format(w))
	print("r2:{}".format(r2))
		


